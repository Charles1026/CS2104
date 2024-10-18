package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

type AtomicSemaphore struct {
	state int32
}

func NewAtomicSemaphore() *AtomicSemaphore {
	return &AtomicSemaphore{state: 1} // Initialize to 1 (unlocked)
}

func (s *AtomicSemaphore) Acquire() {
	// your implementation goes here
	for !atomic.CompareAndSwapInt32(&s.state, 1, 0) {

	}
}

func (s *AtomicSemaphore) Release() {
	// your implementation goes here
	atomic.StoreInt32(&s.state, 1)
}

func main() {
	sem := NewAtomicSemaphore()
	var wg sync.WaitGroup

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			sem.Acquire()
			fmt.Printf("Goroutine %d acquired the semaphore\n", id)
			// Simulate some work
			fmt.Printf("Goroutine %d releasing the semaphore\n", id)
			sem.Release()
		}(i)
	}

	wg.Wait()
	fmt.Println("All goroutines completed")
}
