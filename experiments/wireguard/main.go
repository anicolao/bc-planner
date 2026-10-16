package main

import (
	"crypto/ecdh"
	"crypto/rand"
	"fmt"
	"golang.zx2c4.com/wireguard/device"
	"golang.zx2c4.com/wireguard/tun/netstack"
	"io"
	"net"
	"net/netip"
	"os"
	"strconv"
	"strings"
	"time"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func field(d *device.Device, name string) string {
	s, e := d.IpcGet()
	must(e)
	for _, l := range strings.Split(s, "\n") {
		if strings.HasPrefix(l, name+"=") {
			return strings.TrimPrefix(l, name+"=")
		}
	}
	return ""
}
func main() {
	timer := time.AfterFunc(20*time.Second, func() { fmt.Fprintln(os.Stderr, "local proof timed out"); os.Exit(1) })
	defer timer.Stop()
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
func run() error {
	// Keys are generated in memory for this one test, never emitted or persisted.
	ka, e := ecdh.X25519().GenerateKey(rand.Reader)
	must(e)
	kb, e := ecdh.X25519().GenerateKey(rand.Reader)
	must(e)
	ta, na, e := netstack.CreateNetTUN([]netip.Addr{netip.MustParseAddr("10.77.0.1")}, nil, 1420)
	must(e)
	tb, nb, e := netstack.CreateNetTUN([]netip.Addr{netip.MustParseAddr("10.77.0.2")}, nil, 1420)
	must(e)
	a := device.NewDevice(ta, &loopbackBind{}, device.NewLogger(device.LogLevelSilent, ""))
	defer a.Close()
	b := device.NewDevice(tb, &loopbackBind{}, device.NewLogger(device.LogLevelSilent, ""))
	defer b.Close()
	must(a.IpcSet(fmt.Sprintf("private_key=%x\nlisten_port=0\n", ka.Bytes())))
	must(b.IpcSet(fmt.Sprintf("private_key=%x\nlisten_port=0\n", kb.Bytes())))
	must(a.Up())
	must(b.Up())
	pa, pb := field(a, "listen_port"), field(b, "listen_port")
	must(a.IpcSet(fmt.Sprintf("public_key=%x\nallowed_ip=10.77.0.2/32\nendpoint=127.0.0.1:%s\n", kb.PublicKey().Bytes(), pb)))
	must(b.IpcSet(fmt.Sprintf("public_key=%x\nallowed_ip=10.77.0.1/32\nendpoint=127.0.0.1:%s\n", ka.PublicKey().Bytes(), pa)))
	listener, e := nb.ListenTCP(&net.TCPAddr{IP: net.ParseIP("10.77.0.2"), Port: 8080})
	must(e)
	defer listener.Close()
	done := make(chan error, 1)
	go func() {
		c, e := listener.Accept()
		if e != nil {
			done <- e
			return
		}
		defer c.Close()
		c.SetDeadline(time.Now().Add(10 * time.Second))
		buf := make([]byte, 32)
		n, e := c.Read(buf)
		if e == nil {
			_, e = c.Write(append([]byte("echo:"), buf[:n]...))
		}
		done <- e
	}()
	c, e := na.DialTCP(&net.TCPAddr{IP: net.ParseIP("10.77.0.2"), Port: 8080})
	if e != nil {
		return e
	}
	defer c.Close()
	must(c.SetDeadline(time.Now().Add(10 * time.Second)))
	_, e = c.Write([]byte("wireguard-proof"))
	must(e)
	response := make([]byte, len("echo:wireguard-proof"))
	_, e = io.ReadFull(c, response)
	must(e)
	must(<-done)
	if string(response) != "echo:wireguard-proof" {
		return fmt.Errorf("payload mismatch")
	}
	for i, d := range []*device.Device{a, b} {
		h, e := strconv.ParseInt(field(d, "last_handshake_time_sec"), 10, 64)
		if e != nil || h <= 0 {
			return fmt.Errorf("peer %d missing handshake", i)
		}
		fmt.Printf("peer=%d handshake=verified rx_bytes=%s tx_bytes=%s\n", i, field(d, "rx_bytes"), field(d, "tx_bytes"))
	}
	fmt.Println("PASS: two real WireGuard devices exchanged TCP payload through userspace netstacks over loopback UDP; no external reachability tested")
	return nil
}
