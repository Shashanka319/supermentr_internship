// Student Manager: Using arrays and objects to store student marks and calculate averages

// Array of student objects
let students = [
    {
        name: "Alice",
        marks: [85, 90, 88, 92]
    },
    {
        name: "Bob",
        marks: [78, 82, 79, 85]
    },
    {
        name: "Charlie",
        marks: [95, 93, 97, 89]
    },
    {
        name: "Diana",
        marks: [88, 91, 86, 90]
    }
];

// Function to calculate average marks for a student
function calculateAverage(marks) {
    if (marks.length === 0) return 0;
    let sum = marks.reduce((acc, mark) => acc + mark, 0);
    return sum / marks.length;
}

// Function to display student information with averages
function displayStudents() {
    console.log("Student Marks and Averages:");
    console.log("============================");

    students.forEach(student => {
        let average = calculateAverage(student.marks);
        console.log(`Name: ${student.name}`);
        console.log(`Marks: ${student.marks.join(', ')}`);
        console.log(`Average: ${average.toFixed(2)}`);
        console.log("----------------------------");
    });
}

// Function to add a new student
function addStudent(name, marks) {
    students.push({
        name: name,
        marks: marks
    });
}

// Function to get overall class average
function getClassAverage() {
    let allMarks = students.flatMap(student => student.marks);
    return calculateAverage(allMarks);
}

// Example usage
displayStudents();

console.log(`Class Average: ${getClassAverage().toFixed(2)}`);

// Adding a new student
addStudent("Eve", [87, 89, 91, 88]);
console.log("\nAfter adding Eve:");
displayStudents();