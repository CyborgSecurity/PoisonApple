package main

import (
	"fmt"
	"os"
	"github.com/gen2brain/dlgs"
)

func main() {
	techniqueName := os.Args[1]
	message := fmt.Sprintf("PoisonApple %s persistence mechanism activated!", techniqueName)
	foo, _ :=  dlgs.Info("PoisonApple", message)
	fmt.Println(foo)
}
