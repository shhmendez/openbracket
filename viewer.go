package main
import (
	"os"
	"fmt"
	"github.com/gdamore/tcell"
	"time"
)
func main(){
	tcell.SetEncodingFallback(tcell.EncodingFallbackASCII)
	s, e := tcell.NewScreen()

	if e != nil{
		fmt.Fprintf(os.Stderr, "%v\n",e)
		os.Exit(1)
	}
	if e = s.Init(); e != nil{
		os.Exit(1)
	}
	s.SetStyle(tcell.StyleDefault.Foreground(tcell.ColorBlack).Background(tcell.ColorWheat))
	s.Clear()
	quitChannel := make(chan bool)
	quit := false
	for !quit{
		select {
		case quit = <-quitChannel:
			continue
		case <-time.After(time.Millisecond):
			go poll(s, quitChannel)
			go drawboard(s)
		}		
	}
	s.Fini()

}
func drawboard(screen tcell.Screen,){
	w,h := screen.Size()
	min := h
	if(w < h){
		min = w
	}
	h = min
	h /= 8
	w = h*2
	if w == 0{return}
	x, y := 0,0
	rgb := tcell.NewHexColor(int32(0x0))
	st := tcell.StyleDefault.Background(rgb)

	drawRect(screen, st, x,y,w,h)
	screen.Show()

}
func drawRect(screen tcell.Screen,style tcell.Style, x,y,w,h int){
	for row := 0; row < h; row++{
		for col := 0; col < w; col++{
			screen.SetCell(x+col,y+row,style,' ')
		}
	}
}
func poll(s tcell.Screen, quitChannel chan bool){
		ev := s.PollEvent()
		switch ev := ev.(type){
		case *tcell.EventKey:
			handlekeys(s, ev, quitChannel)
		case *tcell.EventResize:
			s.Sync()
		}
}
func handlekeys(s tcell.Screen, ev *tcell.EventKey, quitChannel chan bool){
	switch ev.Key(){
	case tcell.KeyEscape, tcell.KeyEnter:
			quitChannel <- true
			return
	}
}
