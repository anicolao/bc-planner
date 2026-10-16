package main

import (
	"net"
	"testing"
)

func TestRejectExternalEndpoints(t *testing.T) {
	b := new(loopbackBind)
	for _, s := range []string{"192.0.2.1:1", "[::1]:1", "localhost:1"} {
		if _, e := b.ParseEndpoint(s); e == nil {
			t.Fatalf("accepted %s", s)
		}
	}
	if _, e := b.ParseEndpoint("127.0.0.1:1234"); e != nil {
		t.Fatal(e)
	}
}
func TestRejectPacketMarks(t *testing.T) {
	b := new(loopbackBind)
	if b.SetMark(0) != nil {
		t.Fatal("zero mark")
	}
	if b.SetMark(1) == nil {
		t.Fatal("nonzero mark accepted")
	}
}
func TestClosedBind(t *testing.T) {
	b := new(loopbackBind)
	ep, e := b.ParseEndpoint("127.0.0.1:1")
	if e != nil {
		t.Fatal(e)
	}
	if b.Send([][]byte{[]byte("test")}, ep) != net.ErrClosed {
		t.Fatal("closed bind accepted send")
	}
	if e = b.Close(); e != nil {
		t.Fatal(e)
	}
}
