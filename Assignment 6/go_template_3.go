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
	t.mutex.Lock()

	p.leftFork.Lock()
	p.rightFork.Lock()
	defer p.leftFork.Unlock()
	defer p.rightFork.Unlock()

	t.mutex.Unlock()

	time.Sleep(time.Duration(eatingDuration))
}

func main() {
	table := NewTable()
	fmt.Println("Dinner is starting")
	table.StartDinner(30 * time.Second)
	fmt.Println("Dinner is over")
}
