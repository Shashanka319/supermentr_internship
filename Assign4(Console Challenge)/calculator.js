
function add(a, b) {
    return a + b;


function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}


}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        return "Error: Division by zero";
    }
    return a / b;
}

// Advanced operations
function power(base, exponent) {
    return Math.pow(base, exponent);
}

function squareRoot(number) {
    if (number < 0) {
        return "Error: Cannot take square root of negative number";
    }
    return Math.sqrt(number);
}

function factorial(n) {
    if (n < 0) {
        return "Error: Factorial of negative number";
    }
    if (n === 0 || n === 1) {
        return 1;
    }
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

function percentage(number) {
    return number / 100;
}

function sine(angle) {
    return Math.sin(angle * Math.PI / 180); // Convert to radians
}

function cosine(angle) {
    return Math.cos(angle * Math.PI / 180); // Convert to radians
}

function tangent(angle) {
    return Math.tan(angle * Math.PI / 180); // Convert to radians
}

function logarithm(number) {
    if (number <= 0) {
        return "Error: Logarithm of non-positive number";
    }
    return Math.log10(number);
}

function naturalLog(number) {
    if (number <= 0) {
        return "Error: Natural log of non-positive number";
    }
    return Math.log(number);
}

function exponential(number) {
    return Math.exp(number);
}

function memoryStore() {
    if (currentInput !== '') {
        memory = parseFloat(currentInput);
    }
}

function memoryRecall() {
    currentInput = memory.toString();
    display.value = currentInput;
}

function memoryClear() {
    memory = 0;
}

function memoryAdd() {
    if (currentInput !== '') {
        memory += parseFloat(currentInput);
    }
}

function memorySubtract() {
    if (currentInput !== '') {
        memory -= parseFloat(currentInput);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const display = document.getElementById('display');
    let currentInput = '';
    let operator = '';
    let previousInput = '';

    display.value = '0';

   
    let memory = 0;

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const value = this.textContent.trim();
            const classList = this.classList;

            if (classList.contains('number') || classList.contains('decimal')) {
                if (classList.contains('decimal') && currentInput.includes('.')) {
                    return; // Prevent multiple decimal points
                }
                currentInput += value;
                display.value = currentInput;
            } else if (classList.contains('operator')) {
                let op = value;
                // Map special characters to standard operators
                if (op === '÷') op = '/';
                else if (op === '×') op = '*';
                else if (op === '−') op = '-';

                if (currentInput !== '') {
                    if (previousInput !== '') {
                        calculate();
                    }
                    operator = op;
                    previousInput = currentInput;
                    currentInput = '';
                }
            } else if (classList.contains('equals')) {
                calculate();
            } else if (classList.contains('clear')) {
                clear();
            } else if (classList.contains('backspace')) {
                currentInput = currentInput.slice(0, -1);
                display.value = currentInput || '0';
            } else if (classList.contains('advanced')) {
                const op = this.getAttribute('data-op');
                if (op === 'sqrt' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = squareRoot(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'factorial' && currentInput !== '') {
                    const num = parseInt(currentInput);
                    const result = factorial(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'percentage' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = percentage(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'sin' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = sine(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'cos' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = cosine(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'tan' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = tangent(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'log' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = logarithm(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'ln' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = naturalLog(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'exp' && currentInput !== '') {
                    const num = parseFloat(currentInput);
                    const result = exponential(num);
                    display.value = result;
                    currentInput = result.toString();
                    animateDisplay();
                } else if (op === 'power') {
                    if (currentInput !== '') {
                        operator = '^';
                        previousInput = currentInput;
                        currentInput = '';
                    }
                }
            } else if (classList.contains('memory')) {
                const op = this.getAttribute('data-op');
                if (op === 'mc') {
                    memoryClear();
                } else if (op === 'mr') {
                    memoryRecall();
                } else if (op === 'ms') {
                    memoryStore();
                } else if (op === 'm+') {
                    memoryAdd();
                } else if (op === 'm-') {
                    memorySubtract();
                }
            }
        });  

    document.addEventListener('keydown', function(event) {
        const key = event.key;
        const keyCode = event.keyCode;


        if (key >= '0' && key <= '9') {
            currentInput += key;
            display.value = currentInput;
        }
      
        else if (key === '.') {
            if (!currentInput.includes('.')) {
                currentInput += key;
                display.value = currentInput;
            }
        }
       
        else if (key === '+' || key === '-' || key === '*' || key === '/') {
            if (currentInput !== '') {
                if (previousInput !== '') {
                    calculate();
                }
                operator = key;
                previousInput = currentInput;
                currentInput = '';
            }
        }
        
        else if (key === 'Enter' || key === '=') {
            event.preventDefault();
            calculate();
        }
    
        else if (keyCode === 8) { // Backspace key
            event.preventDefault();
            currentInput = currentInput.slice(0, -1);
            display.value = currentInput || '0';
        }
     
        else if (keyCode === 27 || key.toLowerCase() === 'c') { // Escape or C key
            clear();
        }
      
        else if (key.toLowerCase() === 's') { // S for square root
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = squareRoot(num);
                display.value = result;
                currentInput = result.toString();
            }
        }
        else if (key.toLowerCase() === 'f') { // F for factorial
            if (currentInput !== '') {
                const num = parseInt(currentInput);
                const result = factorial(num);
                display.value = result;
                currentInput = result.toString();
            }
        }
        else if (key === '%') { // % for percentage
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = percentage(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 'i') { // I for sine
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = sine(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 'o') { // O for cosine
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = cosine(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 't') { // T for tangent
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = tangent(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 'l') { // L for logarithm
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = logarithm(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 'n') { // N for natural log
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = naturalLog(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
        else if (key.toLowerCase() === 'e') { // E for exponential
            if (currentInput !== '') {
                const num = parseFloat(currentInput);
                const result = exponential(num);
                display.value = result;
                currentInput = result.toString();
                animateDisplay();
            }
        }
    });
});

    function calculate() {
        if (previousInput !== '' && currentInput !== '' && operator !== '') {
            const prev = parseFloat(previousInput);
            const current = parseFloat(currentInput);
            let result;

            if (isNaN(prev) || isNaN(current)) {
                result = 'Error: Invalid input';
            } else {
                switch (operator) {
                    case '+':
                        result = add(prev, current);
                        break;
                    case '-':
                        result = subtract(prev, current);
                        break;
                    case '*':
                        result = multiply(prev, current);
                        break;
                    case '/':
                        result = divide(prev, current);
                        break;
                    case '^':
                        result = power(prev, current);
                        break;
                    default:
                        result = 'Error: Unknown operator';
                }
            }

            display.value = result;
            currentInput = result.toString();
            previousInput = '';
            operator = '';

           
            animateDisplay();
        }
    }

    function clear() {
        currentInput = '';
        previousInput = '';
        operator = '';
        display.value = '0';
    }

    function animateDisplay() {
        display.style.transform = 'scale(1.02)';
        setTimeout(() => {
            display.style.transform = 'scale(1)';
        }, 150);
    }
});

