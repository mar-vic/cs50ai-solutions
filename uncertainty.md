
# Table of Contents

1.  [Probability](#org1dd4d7b)
    1.  [Possible worlds](#orgae1ba67)
    2.  [Axioms in Probability](#org99bb0bb)
    3.  [Conditional Probability](#org600ffdb)
    4.  [Random Variables](#org016516e)
    5.  [Independence](#org528101c)
2.  [Bayes' Rule](#org8e26ebc)
3.  [Joint Probability](#org16f9db3)


<a id="org1dd4d7b"></a>

# Probability


<a id="orgae1ba67"></a>

## Possible worlds

-   \(\omega\) - some possible situation also called as possible world
    
    For example, rolling a die can result in one of six possible outcomes:
    a world where the die yields a 1, a world where the die yields 2, and
    so on

-   \(P(\omega)\) - the problability of a certain world


<a id="org99bb0bb"></a>

## Axioms in Probability

1.  \(0 < P(\omega) < 1\) - every value representing probability must range between 0 and 1
    -   The problability of 0 represents an impossible event
    -   The probability of 1 represents an event that is certain to happen
    -   In general, the higher the value, the more likely the event is to happen

2.  \(\sum_{\omega \in \Omega} P(\omega) = 1\) - the sum of all probable events equlas to 1


<a id="org600ffdb"></a>

## Conditional Probability

-   Conditional probability is the degree of belief in a
    proposition given some evidence that has already been revealed

-   \(P(a | b)\) - the probability of event \(a\) ocurring given that we know
    that event \(b\) to have ocurred, or, more succinctly, the probability
    of \(a\) given \(b\)

-   \(P(a | b) = \frac{P(a \land b)}{P(b)}\) - the probability of \(a\) given
    \(b\) is equal to probability of \(a\) and \(b\) being true, divided by the 
    probability of \(b\). The following are algebraically equivalent:
    -   \(P(a \land b) = P(b) * P(a | b)\)
    
    -   \(P(a \land b) = P(a) * P(b | a)\)


<a id="org016516e"></a>

## Random Variables

-   A random variable is a variable in probability theory with a domain of
    possible values that it can take on.
    -   Example: to represent possible outcomes when rolling a die, we can
        define a random variable *Roll*, that can take on the fallowing values
        {1, 2, 3, 4, 5, 6}.
    
    -   Example: to represent the status of a flight, we can define a
        variable *Flight* that takes on the values {*on time*, *delayed*, *cancelled*}

-   Probability distribution of a random variable is the assignment of
    probabilities to its all possible values
    -   Example: probablity distribution of random varibale *Roll*:
        -   \(P(Roll = 1) = \frac{1}{6}\)
        -   \(P(Roll = 2) = \frac{1}{6}\)
        -   \(P(Roll = 3) = \frac{1}{6}\)
        -   \(P(Roll = 4) = \frac{1}{6}\)
        -   \(P(Roll = 5) = \frac{1}{6}\)
        -   \(P(Roll = 6) = \frac{1}{6}\)
    
    -   Example: probability distribution of random variable *Flight*:
        -   \(P(Flight = on\ time) = 0.6\)
        -   \(P(Flight = delayed) = 0.3\)
        -   \(P(Flight = cancelled) = 0.1\)


<a id="org528101c"></a>

## Independence

-   Independence is the knowledge that the occurrence of one event does
    not affect the probability of the other event.
    -   Example: when rolling two dice, the result of each die is
        independent from the other.
    
    -   Example: Being cloudy in the morning and the rain occurring in the
        afternoon are depended events. If it is cloudy in the morning, it
        more likely that it will rain in the afternoon.

-   Mathematical definition of independence:
    
    Events \(a\) and \(b\) are independent iff. \(P(a \land b) = P(a)*P(b)\)


<a id="org8e26ebc"></a>

# Bayes' Rule

-   Rule for computing conditional probability

-   \(P(b|a) = \frac{P(b) * P(a|b)}{P(a)}\)


<a id="org16f9db3"></a>

# Joint Probability

-   Joint probability is the likelyhood of multiple events all ocurring

