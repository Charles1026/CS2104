(* In this assessment, we will explore how to use
   LLMs to help us learn a new programming language
   and understand programming language concepts.

   The example language we will explore is SML. You 
   can use your favorite LLM (GPT, Claude, etc) and
   the online SML implementation SOSML, see
   https://sosml.org/editor?0&                   *)

(* QUESTION 1 (10 marks) *)

(* write a datatype Date that consists of an
   integer day, a symbolic month and an integer 
                                            year *)

(* your solution goes here                       *)
datatype month = January | February | March | April | May | June
               | July | August | September | October | November | December;
datatype date = Date of int * month * int;

(* Test cases: if you don't answer this question,
   comment the following before you submit       *)

val myDate = Date(7, September, 2024); 
val myDateValidity: bool = true;
val yourDate = Date(31, December, 1900); 
val yourDateValidity: bool = true;
val theirDate = Date(31, February, 2011);
val theirDateValidity: bool = false;
val negativeDate = Date(~1, February, 2011);
val negativeDateValidity: bool = false;
val negYearDate = Date(1, February, ~2011);
val negYearDateValidity: bool = false;
val leapYearDate = Date(29, February, 2024);
val leapYearDateValidity: bool = true;
val falseLeapYearDate = Date(29, February, 2100);
val falseLeapYearDateValidity: bool = false;
val fourMilLeapYearDate = Date(29, February, 2400);
val fourMilLeapYearDateValidity: bool = true;

(* write a function isValidDate that checks if a
   given date is valid, considering that in leap
   years, the month of February has 29 days, and
   that a leap year is a year that is divisible
   by 4, with the exception that years that are
   divisible by 100 and not by 400 are not leap
   years. Assume that only positive integers are
   used as years.                                *)

(* your solution goes here                       *)
fun isValidDate (Date (day, month, year)): bool = 
  let 
    val isLeapYear: bool = (year mod 4 = 0) andalso (year mod 100 <> 0 orelse year mod 400 = 0);

    val maxDay: int = case month of 
      January  => 31
      | March  => 31
      | May  => 31
      | July  => 31
      | August  => 31
      | October  => 31
      | December  => 31
      | April => 30
      | June => 30
      | September => 30
      | November => 30
      | November => 30
      | February => if isLeapYear then 29 else 28

      (* This produces Elaboration failed: Match rules disagree on type: Records don't agree on members ("5" occurs only once.) for some reason*)
      (* (January, March, May, July, August, October, December) => 31
      | (April, June, September, November) => 30
      | February => if isLeapYear then 29 else 28 *)

  in
    (day > 0 andalso day <= maxDay) andalso year >= 0
  end

(* Test cases: if you don't answer this question,
   uncomment the following before you submit     *)

val isMyDateValid = isValidDate myDate;
print ("My Date is " ^ (if isMyDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isMyDateValid = myDateValidity then "Expected" else "Unexpected") ^ "\n");
val isYourDateValid = isValidDate yourDate;
print ("Your Date is " ^ (if isYourDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isYourDateValid = yourDateValidity then "Expected" else "Unexpected") ^ "\n");
val isTheirDateValid = isValidDate theirDate;
print ("Their Date is " ^ (if isTheirDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isTheirDateValid = theirDateValidity then "Expected" else "Unexpected") ^ "\n");
val isNegativeDateValid = isValidDate negativeDate;
print ("Negative Date is " ^ (if isNegativeDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isNegativeDateValid = negativeDateValidity then "Expected" else "Unexpected") ^ "\n");
val isNegYearDateValid = isValidDate negYearDate;
print ("Negative Year Date is " ^ (if isNegYearDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isNegYearDateValid = negYearDateValidity then "Expected" else "Unexpected") ^ "\n");
val isLeapYearDateValid = isValidDate leapYearDate;
print ("Leap Year Date is " ^ (if isLeapYearDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isLeapYearDateValid = leapYearDateValidity then "Expected" else "Unexpected") ^ "\n");
val isFalseLeapYearDateValid = isValidDate falseLeapYearDate;
print ("False Leap Year Date is " ^ (if isFalseLeapYearDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isFalseLeapYearDateValid = falseLeapYearDateValidity then "Expected" else "Unexpected") ^ "\n");
val isFourMilLeapYearDateValid = isValidDate fourMilLeapYearDate;
print ("Four Millemnium Leap Year Date is " ^ (if isFourMilLeapYearDateValid then "Valid" else "Invalid") ^ ", which is " ^ (if isFourMilLeapYearDateValid = fourMilLeapYearDateValidity then "Expected" else "Unexpected") ^ "\n");

(* QUESTION 2 (6 marks) *)

(* write a generic datatype MyList that can be 
   used to construct lists that are either empty
   (denoted by Empty) or the result of the
   constructor Cons, which takes an element as 
   first argument and a MyList as second.        *)

(* your solution goes here                       *)
datatype 'elemType myList = Empty | Cons of 'elemType * 'elemType myList;


(* Test cases: if you don't answer this question,
   comment the following before you submit       *)

val myList1 = Empty;
val myList2 = Cons(1, Cons(2, Empty));
val myList3 = Cons(fn x => 1, Empty);

(* Define a function myMap that lets you 
   transform a MyList into another MyList by
   applying a generic function to each element 
   as shown in the examples.                     *)

(* your solution goes here                       *)
fun myMap(func: ('a -> 'b)) (inList: 'a myList): 'b myList = 
  case inList of
    Empty => Empty
    | Cons (head, tail) => Cons(func(head), myMap func tail);

(* Test cases: if you don't answer this question,
   comment the following before you submit       *)

val myList1' = myMap (fn x => x + 1) myList1;
val myList2' = myMap (fn x => x + 1) myList2;
val myList3' = myMap (fn x => x 2) myList3;

(* QUESTION 3 (4 marks) *)

(* Imagine you're creating a simple game inventory
   system. Players can collect different types of
   items, each with its own properties. However,
   you want to store all these items in a single
   list for easy management.                     *)

(* let's define three different record types     *)

type weapon = {name: string, damage: int}
type potion = {name: string, healing: int}
type key = {name: string, door: string};

(* Let's create some sample items                *)

val sword = {name = "Steel Sword", 
             damage = 10}
val healPotion = {name = "Health Potion", 
                  healing = 50}
val bossKey = {name = "Golden Key", 
               door = "Boss Room"};

(* Let's try to create a list (or MyList)
   containing all these items                    *)

(* uncomment this out and see what happens *)
(* val inventory = [sword, healPotion, bossKey]; *)
(* val inventory = Cons(sword, 
                        Cons(healPotion, 
                             Cons(bossKey,
                                  Empty)));      *)

(* To solve the problem, we need a common data type
   that can serve as the type of all three kinds of
   items                                         *)

(* Create a data type called item that provides a
   common interface for the three game inventory
   items.                                        *)

(* your solution goes here                       *)
datatype Item = Weapon of weapon | Potion of potion | Key of key;

(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val inventory = [
  Weapon {name = "Steel Sword", damage = 10},
  Potion {name = "Health Potion", healing = 50},
  Key {name = "Golden Key", door = "Boss Room"}
];

(* QUESTION 4 (10 marks) *)

(* Let us say we define a shape datatype
   as follows *)

datatype shape = Shape of {
       (* area of the shape *)
       area: unit -> real, 
       (* name: a string that describes 
                the shape *)
       name: string}

(* Write a function makeCircle to 
   create a circle                               *)

(* your solution goes here                       *)
val makeCircle: (real -> shape) = fn radius: real =>
  Shape {area = fn _ => radius * radius * Math.pi, name = "circle"}

(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val myCircle = makeCircle 5.0;

(* Write a function makeRectangle to 
   create a rectangle                            *)

(* your solution goes here                       *)
fun makeRectangle (side1: real, side2: real) = 
  Shape {area = fn _: unit => side1 * side2, name = "rectangle"}

(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val myRectangle = makeRectangle (7.0, 4.0);

(* Creating a list of shapes                     *)

(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val shapes = [
  makeCircle 5.0,
  makeRectangle (3.0, 4.0),
  makeCircle 2.5
];

(* Define a function totalArea to calculate total 
   area of a list of given shapes. Requirement:
   use the SML function foldl                    *)

(* your solution goes here                       *)
fun totalArea (shps: shape list): real = 
  List.foldl (fn (Shape {area, name}, currSum) => (area ()) + currSum) 0.0 shps;


(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val total = totalArea shapes

(* QUESTION 5 (4 marks) *)

(* Write a function countOccurrences that uses
   SML's functions List.length and List.filter
   to count the occurrences of a given integer n
   in a list of integers. Make sure that your
   function countOccurrences can ONLY be used
   on integers as first argument and lists of
   integers as second argument.                  *)

(* your solution goes here                       *)
fun countOccurrences(n: int) (lst: int list): int = 
  List.length (List.filter (fn (elem: int): int => elem = n) lst);

(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val threeCount =
countOccurrences 3
[1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1];

(* turn your function into a generic function:
   it should be applicable to a list of any type
   of value, not just integers                   *)

(* your solution goes here                       *)
fun countOccurrences' (n: ''a) (lst: ''a list): int = 
  List.length (List.filter (fn (elem: 'a) => elem = n) lst);


(* Test case: if you don't answer this question,
   comment the following before you submit       *)

val threeListCount = countOccurrences'
       [3] [[3,4], [3], [5,6], [3]];

(* Test case: in case you solved Question 3      *)

val bossKeyCount = countOccurrences'
       (Key {name = "Golden Key", 
             door = "Boss Room"})
       inventory;

(* no submission: what kind of restriction does 
   SML impose on the argument types of 
   countOccurrences'? How does the syntax of 
   type variables indicate this restriction?     *)

(* With this knowledge, break the function
   countOccurrences': Apply the function
   to an SML value and a list that contains
   that value as its only element, such that
   the application does not pass the SML
   type checker.                                 *)

val strangeValue = fn _ => 1; (* replace true to
                            get a type error
                            in the application
                            below                *)

(* Reverse test case: The following should
   give a type error                             *)

val givesTypeError = countOccurrences' 
                 strangeValue [strangeValue];
