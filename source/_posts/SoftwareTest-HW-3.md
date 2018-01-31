---
layout: article
title: 【软件测试】作业3 测试之路径覆盖
date: 2017-03-15 23:34:02
tags: 软件测试作业
categories: 作业
---

书上的练习题，要求设计相应的测试用例，写出主路径覆盖
- [Problem Description](#problem)
- [Answer](#answer)
  <!--mo-->
---
<h2 id='problem'>Problem Description</h2>
```
/***********************************
 * Finds and prints n prime integers
 * Jeff Offutt, Spring 2003
************************************/
private static void printPrimes (int n){
	int curPrime;		// Value currently considered for primeness
	int numPrimes;		// Number of primes found so far.
	boolean isPrime;	// Is curPrime prime?
	int [] primes = new int [MAXPRIMES]; // The list of prime numbers.
	// Initialize 2 into the list of primes.
	primes[0] = 2;
	numPrimes = 1;
	curPrime = 2;
	while(numPrimes < n){
		curPrime++;		//next number to consider ...
		isPrime = true;
		for(int i = 0; i <= numPrime-1; i++){
			if(isDivisible(primes[i], curPrime)){
				isPrime = false;
				break;
			}
		}
		if(isPrime){
			primes[numPrimes] = curPrime;
			numPrimes++;
		}
	} // end while
	//Print all the primes out.
	for(int i = 0; i <= numPrimes-1; i ++){
		System.out.println("Prime: "+ primes[i]);
	}
} // end printPrimes
```

> a) Draw the control flow graph for the printPrimes() method.

> b) Consider test cases t1 = (n = 3) and t2 = (n = 5). Although these tour the prime paths in printPrimes(), they do not necessarily find the same faults. Design a simple fault that t2 would be more likely to discover than t1 would.

> c) For printPrimes(), find a test case such that the corresponding test path visits the edge that connects the beginning of the while statement to the for statement without going through the body of the while loop.

> d) Enumerate the test requirements for node coverage, edge coverage, and prime path coverage for the graph for printPrimes().

---
<h2 id='answer'>Answer</h2>
##### a) Draw the control flow graph for the printPrimes() method.
![pictures](/images/2017-3-14-23-28.png)

##### b) Consider test cases t1 = (n = 3) and t2 = (n = 5). Although these tour the prime paths in printPrimes(), they do not necessarily find the same faults. Design a simple fault that t2 would be more likely to discover than t1 would.
> If constant variable `MAXPRIMES` equals 4,it will occur a fault when n equals 5 but will not if n equals 3.

##### c) For printPrimes(), find a test case such that the corresponding test path visits the edge that connects the beginning of the while statement to the for statement without going through the body of the while loop.

> Let n = 1, and it will break the while loop in the first iteration.

##### d) Enumerate the test requirements for node coverage, edge coverage, and prime path coverage for the graph for printPrimes().
node coverage

> {1,2,3,4,5,6,7,8,9,10,11,12,13,14}

edge coverage

> {(1,2), (2,3), (2,10), (3,4), (4,5), (5,6), (5,8), (6,5), (6,7), (7,8), (8,2), (9,2), (10,11), (11,12), (11,14), (12,13), (13,11)}

prime path coverage

> {(1,2,3,4,5,6,7),
> (1,2,3,4,5,6,8,9,10,11),
> (1,2,3,4,5,6,8,9,11),
> (1,2,3,4,5,9,10,11),
> (1,2,3,4,5,9,11),
> (1,2,12,13,14,15),
> (1,2,12,16),
> (2,3,4,5,6,8,9,10,11,2),
> (2,3,4,5,6,8,9,11,2),
> (2,3,4,5,9,10,11,2),
> (2,3,4,5,9,11,2),
> (3,4,5,6,8,9,10,11,2,12,13,14,15),
> (3,4,5,6,8,9,11,2,12,13,14,15),
> (3,4,5,6,8,9,10,11,2,12,13,16),
> (3,4,5,6,8,9,11,2,12,13,16),
> (3,4,5,9,10,11,2,12,13,14,15),
> (3,4,5,9,11,2,12,13,14,15),
> (3,4,5,9,10,11,2,12,13,16),
> (3,4,5,9,11,2,12,13,16),
> (5,6,7,5),
> (6,7,5,9,10,11,2,12,13,14,15),
> (6,7,5,9,11,2,12,13,14,15),
> (6,7,5,9,10,11,2,12,13,16),
> (6,7,5,9,11,2,12,13,16),
> (13,14,15,13),
> (14,15,13,16)}

##### e) Design a test case to coverage prime path using JUnit.
Main.java
```
public class Main {
    private static final int MAXPRIMES = 5;
    public static void main(String args[]){
        printPrimes(5);
    }
    private static boolean isDivisible(int a, int b){
        if(b % a == 0)
            return true;
        return false;
    }
    public static int[] printPrimes (int n){
        int curPrime;		// Value currently considered for primeness
        int numPrimes;		// Number of primes found so far.
        boolean isPrime;	// Is curPrime prime?
        int [] primes = new int [MAXPRIMES]; // The list of prime numbers.
        // Initialize 2 into the list of primes.
        primes[0] = 2;
        numPrimes = 1;
        curPrime = 2;
        while(numPrimes < n){
            curPrime++;		//next number to consider ...
            isPrime = true;
            for(int i = 0; i <= numPrimes-1; i++){
                if(isDivisible(primes[i], curPrime)){
                    isPrime = false;
                    break;
                }
            }
            if(isPrime){
                primes[numPrimes] = curPrime;
                numPrimes++;
            }
        } // end while
        //Print all the primes out.
        for(int i = 0; i <= numPrimes-1; i ++){
            System.out.println("Prime: "+ primes[i]);
        }
        return primes;
    } // end printPrimes
}
```
MainTest.java
```
import org.junit.Test;
import static org.junit.Assert.*;
/**
 * Created by hardy on 17-3-15.
 */
public class MainTest {
    @Test
    public void printPrimes() throws Exception {
        int [] a = new int [] {2, 3, 5, 7, 11};
        assertArrayEquals(a, Main.printPrimes(5));
    }
}
```
![pictures](/images/2017-3-15-00-15.png)

---
