package main

import (
	"fmt"
	"sync"
)

type Account struct {
	balance int
	mu      sync.Mutex
}

func NewAccount(initialBalance int) *Account {
	return &Account{
		balance: initialBalance,
	}
}

func (a *Account) Deposit(amount int) {
	// your implementation goes here
	a.mu.Lock()
	a.balance += amount
	a.mu.Unlock()
}

func (a *Account) Withdraw(amount int) (bool, int) {
	// your implementation goes here
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.balance >= amount {
		a.balance -= amount
		return true, a.balance
	}
	return false, a.balance
}

func (a *Account) Balance() int {
	// your implementation goes here
	a.mu.Lock()
	defer a.mu.Unlock()
	return a.balance
}

func main() {
	account := NewAccount(0)
	var wg sync.WaitGroup

	// Simulate concurrent deposits and withdrawals
	for i := 0; i < 50; i++ {
		wg.Add(2)
		go func() {
			defer wg.Done()
			account.Deposit(50)
		}()
		go func() {
			defer wg.Done()
			success, amount := account.Withdraw(30)
			if success {
				fmt.Printf("Withdrawn: %d\n", amount)
			} else {
				fmt.Println("Withdrawal failed")
			}
		}()
	}

	wg.Wait()
	fmt.Printf("Final balance: %d\n", account.Balance())
}
