package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const (
	numberOfPhilosophers = 5
	eatingDuration       = 3 * time.Second
	thinkingDuration     = 3 * time.Second
)

type Fork struct{ sync.Mutex }

type Philosopher struct {
	id                  int
	leftFork, rightFork *Fork
}

type Table struct {
	forks        []*Fork
	philosophers []*Philosopher
	mutex        sync.Mutex
}

func NewTable() *Table {
	t := &Table{
		forks:        make([]*Fork, numberOfPhilosophers),
		philosophers: make([]*Philosopher, numberOfPhilosophers),
	}
	for i := 0; i < numberOfPhilosophers; i++ {
		t.forks[i] = &Fork{}
	}
	for i := 0; i < numberOfPhilosophers; i++ {
		t.philosophers[i] = &Philosopher{
			id:        i,
			leftFork:  t.forks[i],
			rightFork: t.forks[(i+1)%numberOfPhilosophers],
		}
	}
	return t
}

func (t *Table) StartDinner(duration time.Duration) {
	var wg sync.WaitGroup
	for _, p := range t.philosophers {
		wg.Add(1)
		go func(p *Philosopher) {
			defer wg.Done()
			for start := time.Now(); time.Since(start) < duration; {
				p.think()
				t.eat(p)
			}
		}(p)
	}
	wg.Wait()
}

func (p *Philosopher) think() {
	fmt.Printf("Philosopher %d is thinking\n", p.id)
	time.Sleep(time.Duration(rand.Intn(int(thinkingDuration))))
}

func (t *Table) eat(p *Philosopher) {
// your implementation goes here
	if !t.forks[p.id].TryLock() { // try lock left fork
		return // return to try again
	}
	defer t.forks[p.id].Unlock() // We successfully got the left fork, unlock after return

	if !t.forks[(p.id + 1) % numberOfPhilosophers].TryLock() { // try lock right fork
		return // return to try again
	}
	defer t.forks[(p.id + 1) % numberOfPhilosophers].Unlock() // We successfully got the right fork, unlock after return

	fmt.Printf("Philosopher %d is eating\n", p.id)
}

func main() {
	table := NewTable()
	fmt.Println("Dinner is starting")
	table.StartDinner(30 * time.Second)
	fmt.Println("Dinner is over")
}
