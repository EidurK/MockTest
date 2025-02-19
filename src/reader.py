import json

def initialize_json_file(filepath):
    with open(filepath, 'w') as file:
        json.dump([], file)

def read_facts(filepath):
    with open(filepath, 'r') as file:
        facts = json.load(file)
        return facts

def add_fact(fact, filepath):
    with open(filepath, 'r') as file:
        facts = json.load(file)
    
    facts.append(fact)
    
    with open(filepath, 'w') as file:
        json.dump(facts, file)

def print_facts(filepath):
    with open(filepath, 'r') as file:
        facts = json.load(file)
    
    for fact in facts:
        print(json.dumps(fact))

file = '../data/Facts.json'
facts = [
r"""Determine $\frac{dy}{dx}$ where $y=\ln(\sin(x))$""",
r"""Determine the Taylor-polynomial of degree 2 and centre 0 fro the function $f(x) = (1+x)^{-10}$""",
r"""Determine the limit $\lim_{x\rightarrow 0}\frac{1-\cos(x)}{x^2\cos(x)}$""",
r"""Determine the integral $\int \frac{1}{x\sqrt{\ln(x)}} dx$""",
r"""
Consider a relation 𝑅(𝐴, 𝐵, 𝐶, 𝐷, 𝐸) and a collection of functional
dependencies (FD’s) 𝐹 = {𝐵 → 𝐸, 𝐵 → 𝐴, 𝐶𝐸 → 𝐵, 𝐶 → 𝐷}
What is the closure of 𝐵𝐶 in relation to 𝐹?
""",
r"""
Consider a relation 𝑅(𝐴, 𝐵, 𝐶, 𝐷, 𝐸) and a collection of functional
dependencies (FD’s) 𝐹 = {𝐵 → 𝐸, 𝐵 → 𝐴, 𝐶𝐸 → 𝐵, 𝐶 → 𝐷}
What are all the candidate keys of 𝑅?
""",
r"""
A relation $R$ is in Boyce-Codd Normal Form (BCNF) if for all functional
dependencies $X \rightarrow Y$ within $R$ either $X$ is a superkey of $R$ or $X \rightarrow Y$ is
trivial.
""",
r"""
EBITDA is widely used when assessing the performance of a company. EBITDA is useful to assess the underlying profitability of the operating businesses alone, i.e. how much profit the business generates by providing the services, selling the goods etc. in the given time period.
""",
r"""
Find $x$ where 
$$3x * 4 + 2x = 15$$
""",
r"""
What is the primary function of the convolutional layer in a Convolu-
tional Neural Network (CNN)?
""",
r"""
(4 points) Pat and Mat are training linear regression models using the same
data set.
(a) (2 points) Pat’s model is better since it has a lower training error than
Mat’s model. Do you agree with this sentence? Briefly explain your answer.
(b) (2 points) Pat and Mat add a regularisation term to the square loss
function. They put weight λ > 0 on the regularisation term and choose the
best λ based on the test set. Do you agree with the steps Pat and Mat took?
Briefly explain your answer
""",
r"""
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
""",
r"""
public abstract class Car {
    private String model;
    private int year;

    public Car(String make, String model, int year) {
        this.model = model;
        this.year = year;
    }

    public String getModel() {
        return model;
    }

    public int getYear() {
        return year;
    }

    public abstract void startEngine();
    public abstract void stopEngine();
}
""",
r"""
An abstract class in object-oriented programming is a class that cannot be instantiated on 
its own and is designed to be subclassed. It often contains one or more abstract methods, 
which are methods declared without an implementation. Subclasses of the abstract class are 
required to provide implementations for these abstract methods. Abstract classes are used 
to define a common interface and share code among related classes, promoting code reuse and
enforcing a contract for subclasses. They are a key feature in languages like Java, C++, 
and Python.
""",
r"""
The four types of bases found in a DNA molecule: adenine (A), cytosine (C), guanine (G), and thymine (T).
""",
r"""
How often will the following funcition print foo?

def func(n):
    for i in range(n):
        for j in range(i):
            print("foo")
""",
r"""
An activation record is the memory area that a single activation of a function or procedure uses while it is running. 
""",
r"""
What is the slope of a line defined with the following function
$$
y = 3x + 2
$$
""",
r"""
What is the slope of the following function at $x = 4$.
$$
f(x) = 2x^2 + 3x + 1
$$
""",
r"""
Calculate $\frac{3^8}{3^2 \cdot 3}$.
""",
r"""
What is the output of the following code snippet
x = 39
print(x//2)
""",
r"""
private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi)
{
	for(int k = lo; k < hi; k++) aux[k] = a[k];
	int i = lo;
	int j = mid +1;
	for(int k = lo; k < hi; k++){
		if(i > mid) a[k] = aux[j++];
		else if(j > hi) a[k] = aux[i++];
		else if(less(aux[j], aux[i]) a[k] = aux[j++];
		else a[k] = aux[i++];
	}
}
""",
r"""
$$
x^2 + 8x + 16 = (x + 4)(x + 4)
$$
"""



        ]
initialize_json_file(file)
for fact in facts:
    add_fact(fact, file)




