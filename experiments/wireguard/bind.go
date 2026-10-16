package main

import (
	"encoding/binary"
	"fmt"
	"golang.zx2c4.com/wireguard/conn"
	"net"
	"net/netip"
	"sync"
)

// loopbackBind is an intentionally IPv4-loopback-only transport for this proof.
// It implements WireGuard's public Bind interface with ordinary UDP, without
// interface discovery, sticky source routing, marks or privileged sockets.
type loopbackBind struct {
	mu     sync.Mutex
	socket *net.UDPConn
}
type endpoint struct{ addr netip.AddrPort }

func (e *endpoint) ClearSrc()           {}
func (e *endpoint) SrcToString() string { return "" }
func (e *endpoint) DstToString() string { return e.addr.String() }
func (e *endpoint) DstIP() netip.Addr   { return e.addr.Addr() }
func (e *endpoint) SrcIP() netip.Addr   { return netip.Addr{} }
func (e *endpoint) DstToBytes() []byte {
	b := e.addr.Addr().AsSlice()
	return binary.BigEndian.AppendUint16(b, e.addr.Port())
}
func (b *loopbackBind) BatchSize() int { return 1 }
func (b *loopbackBind) SetMark(mark uint32) error {
	if mark != 0 {
		return fmt.Errorf("packet marks unsupported")
	}
	return nil
}
func (b *loopbackBind) ParseEndpoint(s string) (conn.Endpoint, error) {
	a, e := netip.ParseAddrPort(s)
	if e != nil {
		return nil, e
	}
	if !a.Addr().Is4() || !a.Addr().IsLoopback() {
		return nil, fmt.Errorf("only IPv4 loopback is allowed")
	}
	return &endpoint{a}, nil
}
func (b *loopbackBind) Open(port uint16) ([]conn.ReceiveFunc, uint16, error) {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.socket != nil {
		return nil, 0, conn.ErrBindAlreadyOpen
	}
	s, e := net.ListenUDP("udp4", &net.UDPAddr{IP: net.IPv4(127, 0, 0, 1), Port: int(port)})
	if e != nil {
		return nil, 0, e
	}
	b.socket = s
	receive := func(p [][]byte, sizes []int, eps []conn.Endpoint) (int, error) {
		n, a, e := s.ReadFromUDPAddrPort(p[0])
		if e != nil {
			return 0, e
		}
		sizes[0] = n
		eps[0] = &endpoint{a}
		return 1, nil
	}
	return []conn.ReceiveFunc{receive}, uint16(s.LocalAddr().(*net.UDPAddr).Port), nil
}
func (b *loopbackBind) Close() error {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.socket == nil {
		return nil
	}
	e := b.socket.Close()
	b.socket = nil
	return e
}
func (b *loopbackBind) Send(bufs [][]byte, ep conn.Endpoint) error {
	b.mu.Lock()
	s := b.socket
	b.mu.Unlock()
	if s == nil {
		return net.ErrClosed
	}
	e, ok := ep.(*endpoint)
	if !ok {
		return conn.ErrWrongEndpointType
	}
	for _, p := range bufs {
		if _, err := s.WriteToUDPAddrPort(p, e.addr); err != nil {
			return err
		}
	}
	return nil
}
