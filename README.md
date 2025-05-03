# Timetable-Generator-with-Frontend


## Description

The University Scheduling System is an automated timetable generation tool designed to optimize class scheduling while resolving conflicts related to faculty availability, classroom constraints, and overlapping time slots. Built using C++ and advanced data structures, it ensures efficient resource allocation and minimizes administrative workload. Future enhancements include an improved frontend for a better user experience.

## Group Members

1. Muneeb Jawed
2. Ibrahim Saqib
3. Rafay Rauf

## Features

✅ Automated timetable generation

✅ Conflict detection & resolution

✅ Optimized scheduling using graphs & backtracking

✅ Persistent storage for schedule data

✅ User-friendly interface (Frontend improvements planned)


## Tech Stack

Backend: C++
Frontend: (To be decided, replacing HTML/CSS)
Libraries: STL, File I/O, Boost (optional)
Database: SQLite/MySQL (optional for future versions)


## Installation & Setup

Clone the Repository
```
git clone https://github.com/your-username/Timetable-Generator-with-Frontend.git
cd Timetable-Generator-with-Frontend
```
Set Up the Development Environment
Ensure you have a C++ compiler (GCC, MinGW, or Visual Studio).

Compile the Code
```
g++ -o scheduler main.cpp
```
Run the Program
```
./scheduler
```

## How to Contribute

Fork the repository.
Create a new branch for your feature:
```
git checkout -b feature-branch
```
Make changes and commit:
```
git add .
git commit -m "Added new feature"
```
Push your branch and create a pull request!


# Milestone 2

## Objective
To demonstrate working implementations of core data structures with sample input/output and showcase their practical relevance to the problem domain.

## Implemented Data Structures

### 1. AVL Tree
Used to store and manage course information.
Maintains balanced height to ensure efficient searching and insertion.
Each node contains a Course object with a unique ID, course code, credit hours, and semester.
### 2. Linked List
Used to manage ordered integer elements (e.g., student roll numbers or course slots).
Supports insertions and deletions at any point efficiently.
### 3. Queue
Used for task or schedule handling (e.g., student registration queue or time-slot allocation).
Implements standard enqueue and dequeue operations.

## Efficiency Analysis

| Data Structure | Time Complexity (Best/Average/Worst)     | Space Complexity |
|----------------|-------------------------------------------|------------------|
| AVL Tree       | O(log n) / O(log n) / O(log n)            | O(n)             |
| Linked List    | O(1) insert/delete at head, O(n) search   | O(n)             |
| Queue (Array)  | O(1) enqueue/dequeue (amortized)          | O(n)             |

## Application of class concepts

This project integrates:

  - Balanced trees (AVL) for optimized searching and updates.
  - Dynamic memory via linked structures.
  - Queue-based processing to simulate real-time task handling.
  - Modular OOP principles with constructors, encapsulation, and separation of concerns.


## Progress on the project

Below is a sample of the code that is to be implemented in the backend. There will be upcoming changes made to the code in the future along with the code for the frontend (which is still a work in progress). Run the code inside any C++ compiler, but make sure to have the courses_info.txt file downloaded in the same location with the C++ file.

```
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <fstream>
#include <limits>
#include <algorithm>
using namespace std;

const vector<string> DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};
const vector<string> CLASSROOMS = {"LH1", "LH2", "LH3", "LH4", "LH5", "LH6", "LH7", "LH8"};
const int SLOTS_PER_DAY = 8;

// Helper functions for string trimming and case conversion
string toLowerCase(const string& str) {
    string result = str;
    transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

string trim(const string& str) {
    size_t first = str.find_first_not_of(" \t\n\r\f\v");
    if (first == string::npos)
        return "";
    size_t last = str.find_last_not_of(" \t\n\r\f\v");
    return str.substr(first, (last - first + 1));
}

struct Course {
    string courseName;
    string instructor;
    string speciality;
    int duration;
    int creditHours; // New field for credit hours
};

struct Slot {
    string courseName;
    string instructor;
    string speciality;
    string classroom;
    string day;
    int slot;
};

class Node {
public:
    Course course;
    Node* left;
    Node* right;
    int height;

    Node(Course c) : course(c), left(nullptr), right(nullptr), height(1) {}
};

class AVLTree {
private:
    Node* root;

    int getHeight(Node* node) {
        return node == nullptr ? 0 : node->height;
    }

    int getBalanceFactor(Node* node) {
        return node == nullptr ? 0 : getHeight(node->left) - getHeight(node->right);
    }

    Node* rightRotate(Node* y) {
        Node* x = y->left;
        Node* T2 = x->right;

        x->right = y;
        y->left = T2;

        y->height = std::max(getHeight(y->left), getHeight(y->right)) + 1;
        x->height = std::max(getHeight(x->left), getHeight(x->right)) + 1;

        return x;
    }

    Node* leftRotate(Node* x) {
        Node* y = x->right;
        Node* T2 = y->left;

        y->left = x;
        x->right = T2;

        x->height = std::max(getHeight(x->left), getHeight(x->right)) + 1;
        y->height = std::max(getHeight(y->left), getHeight(y->right)) + 1;

        return y;
    }

    Node* insert(Node* node, Course course) {
        if (node == nullptr) {
            return new Node(course);
        }

        if (course.courseName < node->course.courseName) {
            node->left = insert(node->left, course);
        } else if (course.courseName > node->course.courseName) {
            node->right = insert(node->right, course);
        } else {
            return node; // Duplicate course names not allowed
        }

        node->height = 1 + std::max(getHeight(node->left), getHeight(node->right));

        int balance = getBalanceFactor(node);

        if (balance > 1 && course.courseName < node->left->course.courseName) {
            return rightRotate(node);
        }

        if (balance < -1 && course.courseName > node->right->course.courseName) {
            return leftRotate(node);
        }

        if (balance > 1 && course.courseName > node->left->course.courseName) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        if (balance < -1 && course.courseName < node->right->course.courseName) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        return node;
    }

    Node* deleteNode(Node* root, std::string courseName) {
        if (root == nullptr) {
            return root;
        }

        if (courseName < root->course.courseName) {
            root->left = deleteNode(root->left, courseName);
        } else if (courseName > root->course.courseName) {
            root->right = deleteNode(root->right, courseName);
        } else {
            if ((root->left == nullptr) || (root->right == nullptr)) {
                Node* temp = root->left ? root->left : root->right;
                if (temp == nullptr) {
                    temp = root;
                    root = nullptr;
                } else {
                    *root = *temp;
                }
                delete temp;
            } else {
                Node* temp = getMinValueNode(root->right);
                root->course = temp->course;
                root->right = deleteNode(root->right, temp->course.courseName);
            }
        }

        if (root == nullptr) {
            return root;
        }

        root->height = 1 + std::max(getHeight(root->left), getHeight(root->right));
        int balance = getBalanceFactor(root);

        if (balance > 1 && getBalanceFactor(root->left) >= 0) {
            return rightRotate(root);
        }

        if (balance > 1 && getBalanceFactor(root->left) < 0) {
            root->left = leftRotate(root->left);
            return rightRotate(root);
        }

        if (balance < -1 && getBalanceFactor(root->right) <= 0) {
            return leftRotate(root);
        }

        if (balance < -1 && getBalanceFactor(root->right) > 0) {
            root->right = rightRotate(root->right);
            return leftRotate(root);
        }

        return root;
    }

    Node* getMinValueNode(Node* node) {
        Node* current = node;
        while (current->left != nullptr) {
            current = current->left;
        }
        return current;
    }

    void inOrder(Node* node, std::vector<Course>& courses) {
        if (node != nullptr) {
            inOrder(node->left, courses);
            courses.push_back(node->course);
            inOrder(node->right, courses);
        }
    }

    Node* search(Node* node, std::string courseName) {
        if (node == nullptr || node->course.courseName == courseName) {
            return node;
        }
        if (courseName < node->course.courseName) {
            return search(node->left, courseName);
        }
        return search(node->right, courseName);
    }

    void freeNodes(Node* node) {
        if (node != nullptr) {
            freeNodes(node->left);
            freeNodes(node->right);
            delete node;
        }
    }

public:
    AVLTree() : root(nullptr) {}

    ~AVLTree() {
        freeNodes(root);
    }

    void insertCourse(Course course) {
        root = insert(root, course);
    }

    void deleteCourse(std::string courseName) {
        root = deleteNode(root, courseName);
    }

    void getAllCourses(std::vector<Course>& courses) {
        inOrder(root, courses);
    }

    void searchCourse(std::string courseName) {
        Node* result = search(root, courseName);
        if (result != nullptr) {
            std::cout << "Course found: " << result->course.courseName << ", Instructor: " << result->course.instructor << ", Speciality: " << result->course.speciality << ", Duration: " << result->course.duration << " hours, Credit Hours: " << result->course.creditHours << std::endl;
        } else {
            std::cout << "Course not found." << std::endl;
        }
    }
};


class ListNode {
public:
    int data;
    ListNode* next;

    ListNode(int val) : data(val), next(nullptr) {}
};

class LinkedList {
private:
    ListNode* head;

public:
    LinkedList() : head(nullptr) {}

    void insertAtEnd(int val) 
    {
        ListNode* newNode = new ListNode(val);
        if (!head)
         {
            head = newNode;
        }
         else
         {
            ListNode* temp = head;
            while (temp->next) {
                temp = temp->next;
            }
            temp->next = newNode;
        }
    }

    void insertAtStart(int val)
    {
        ListNode* newNode = new ListNode(val);
        newNode->next = head;
        head = newNode;
    }

    void insertAtPosition(int val, int pos)
    {
        ListNode* newNode = new ListNode(val);
        if (pos == 0) {
            newNode->next = head;
            head = newNode;
            return;
        }
        ListNode* temp = head;
        for (int i = 0; temp != nullptr && i < pos - 1; i++) {
            temp = temp->next;
        }
        if (temp == nullptr) {
            cout << "Position out of bounds!" << endl;
            return;
        }
        newNode->next = temp->next;
        temp->next = newNode;
    }

    void deleteFromStart() 
    {
        if (!head) {
            cout << "List is empty!" << endl;
            return;
        }
        ListNode* temp = head;
        head = head->next;
        delete temp;
    }

    void deleteFromEnd()
    {
        if (!head) {
            cout << "List is empty!" << endl;
            return;
        }
        if (!head->next)
        {
            delete head;
            head = nullptr;
            return;
        }
        ListNode* temp = head;
        while (temp->next->next)
        {
            temp = temp->next;
        }
        delete temp->next;
        temp->next = nullptr;
    }

    void deleteFromPosition(int pos)
    {
        if (!head) {
            cout << "List is empty!" << endl;
            return;
        }
        if (pos == 0)
        {
            ListNode* temp = head;
            head = head->next;
            delete temp;
            return;
        }
        ListNode* temp = head;
        for (int i = 0; temp != nullptr && i < pos - 1; i++) 
        {
            temp = temp->next;
        }
        if (temp == nullptr || temp->next == nullptr)
        {
            cout << "Position out of bounds!" << endl;
            return;
        }
        ListNode* toDelete = temp->next;
        temp->next = toDelete->next;
        delete toDelete;
    }

    void reverse()
     {
        ListNode* prev = nullptr;
        ListNode* current = head;
        ListNode* next = nullptr;
        while (current)
         {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        head = prev;
    }

    void search(int val)
     {
        ListNode* temp = head;
        int position = 0;
        while (temp)
         {
            if (temp->data == val)
             {
                cout << "Value " << val << " found at position " << position << endl;
                return;
            }
            temp = temp->next;
            position++;
        }
        cout << "Value " << val << " not found in the list." << endl;
    }

    void display() {
        ListNode* temp = head;
        while (temp)
         {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
};


class QueueNode {
public:
    int data;

    QueueNode* next;

    QueueNode(int val) : data(val), next(nullptr) {}
};


class Queue {
private:
    QueueNode* front;
    QueueNode* rear;

public:
    Queue() : front(nullptr), rear(nullptr) {}

    void enqueue(int val)
     {
        QueueNode* newNode = new QueueNode(val);
        if (!rear) 
        {
            front = rear = newNode;
        } else
         {
            rear->next = newNode;
            rear = newNode;
        }
    }

    void dequeue()
     {
        if (!front)
         {
            cout << "Queue is empty!" << endl;
            return;
        }
        QueueNode* temp = front;
        front = front->next;
        if (!front)
         {
            rear = nullptr;
        }
        delete temp;
    }

    int peek()
     {
        if (!front)
         {
            cout << "Queue is empty!" << endl;
            return -1;
        }
        return front->data;
    }

    bool isEmpty()
     {
        return front == nullptr;
    }

    void reverse() 
    {
        if (!front) return;
        QueueNode* prev = nullptr;
        QueueNode* current = front;
        QueueNode* next = nullptr;
        rear = front;
        while (current) {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        front = prev;
    }

    void display()
     {
        QueueNode* temp = front;
        while (temp) {
            cout << temp->data << " <- ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }

    int size()
     {
        int count = 0;
        QueueNode* temp = front;
        while (temp) {
            count++;
            temp = temp->next;
        }
        return count;
    }
};

// Additional functions added for comprehensive coverage.

class Scheduler
 {
private:
    AVLTree courseTree;
    map<string, vector<vector<Slot>>> timetable;
    map<string, string> instructorNameMap; // lowercase -> canonical case

    bool isSlotAvailable(const string& day, int roomIndex, int slotIndex)  //check any slot avaliable
     {
        return timetable[day][roomIndex][slotIndex].courseName.empty();
    }

    bool isInstructorAvailable(const string& instructor, const string& day, int slotIndex) //check instructor ava;aoble
    {
        string instructorLower = toLowerCase(trim(instructor));
        for (size_t room = 0; room < CLASSROOMS.size(); ++room) 
        {
            if (toLowerCase(trim(timetable[day][room][slotIndex].instructor)) == instructorLower)
             {
                return false;
            }
        }
        return true;
    }

    void detectConflicts() {    //slots should not be same at same time
        map<string, set<pair<string, int>>> instructorSchedule;
        for (const auto& day : DAYS)
         {
            for (size_t room = 0; room < CLASSROOMS.size(); ++room)
             {
                for (int slot = 0; slot < SLOTS_PER_DAY; ++slot)
                 {
                    const auto& slotData = timetable[day][room][slot];
                    if (!slotData.instructor.empty()) 
                    {
                        auto& schedule = instructorSchedule[slotData.instructor];
                        if (!schedule.insert({day, slot}).second) 
                        {
                            cout << "Conflict detected for instructor " << slotData.instructor << " on " << day << ", Slot " << slot + 1 << " in Classroom " << CLASSROOMS[room] << endl;
                        }
                    }
                }
            }
        }
    }


void saveTimetableToFile() {
    ofstream htmlFile("timetable.html");
    if (!htmlFile) {
        cerr << "Error: Unable to open file for writing timetable." << endl;
        return;
    }

    htmlFile << "<!DOCTYPE html><html><head><title>University Timetable</title>";
    htmlFile << "<style>";

    htmlFile << "table {border-collapse: collapse; width: 100%;}";

    htmlFile << "th, td {border: 1px solid black; padding: 8px; text-align: center;}";

    htmlFile << "th {background-color: #f2f2f2;}";

    htmlFile << "</style></head><body>";

    htmlFile << "<h1>University Timetable</h1>";

    htmlFile << "<table><tr><th>Day</th><th>Slot</th>";

    for (const auto& classroom : CLASSROOMS) 
    {
        htmlFile << "<th>" << classroom << "</th>";
    }

    htmlFile << "</tr>";

    for (const auto& day : DAYS) {
        for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) 
        {
            htmlFile << "<tr>";
            if (slot == 0) 
            {
                htmlFile << "<td rowspan='" << SLOTS_PER_DAY << "'>" << day << "</td>";
            }
            htmlFile << "<td>Slot " << slot + 1 << "</td>";

            for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
                const auto& slotData = timetable[day][room][slot];
                if (!slotData.courseName.empty()) {
                    htmlFile << "<td>" << slotData.courseName << " (" << slotData.instructor << ")</td>";
                } else {
                    htmlFile << "<td>Free</td>";
                }
            }
            htmlFile << "</tr>";
        }
    }

    htmlFile << "</table></body></html>";

    htmlFile.close();

    cout << "Timetable saved to timetable.html successfully." << endl;
}

    void allocateCourse(const Course& course, size_t startDayIndex = 0)    //allocate courses according to their day/classroom/slots(credit hours)
     {
        int classesRemaining = course.creditHours;
        size_t dayIndex = startDayIndex;
        size_t daysCount = DAYS.size();
        int noAllocationCount = 0;
        while (classesRemaining > 0) {
            const string& day = DAYS[dayIndex];
            bool allocated = false;
            for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
                for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) {
                    if (isSlotAvailable(day, room, slot) && isInstructorAvailable(course.instructor, day, slot)) {
                timetable[day][room][slot] = {
                    course.courseName, toLowerCase(trim(course.instructor)), course.speciality, CLASSROOMS[room], day, slot
                };
                        --classesRemaining; // reduce credit hour after allocating
                        allocated = true;
                        break;
                    }
                }
                if (allocated) break;
            }
            if (!allocated) {
                noAllocationCount++;
                if (noAllocationCount >= (int)daysCount) {
                    cout << "Unable to allocate all classes for course: " << course.courseName << ". Please check availability and try again." << endl;
                    break;
                }
            } else {
                noAllocationCount = 0;
            }
            dayIndex = (dayIndex + 1) % daysCount;
        }
    }

public:
    Scheduler() {
        for (const auto& day : DAYS) {
            timetable[day] = vector<vector<Slot>>(CLASSROOMS.size(), vector<Slot>(SLOTS_PER_DAY));
        }
    }

    void clearScheduleForDay(const string& dayInput) {
        string day = dayInput;
        transform(day.begin(), day.end(), day.begin(), ::tolower);
        map<string, string> dayMap = {
            {"monday", "Monday"},
            {"tuesday", "Tuesday"},
            {"wednesday", "Wednesday"},
            {"thursday", "Thursday"},
            {"friday", "Friday"}
        };
        if (dayMap.find(day) == dayMap.end()) {
            cout << "Invalid day: " << dayInput << endl;
            return;
        }
        string properDay = dayMap[day];
        for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
            for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) {
                timetable[properDay][room][slot] = Slot{};
            }
        }
        cout << "Schedule cleared for " << properDay << "." << endl;
    }

    void clearScheduleForAllDays() {
        for (const auto& day : DAYS) {
            for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
                for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) {
                    timetable[day][room][slot] = Slot{};
                }
            }
        }
        cout << "Schedule cleared for all days." << endl;
    }

    void editScheduleForDay(const std::string& dayInput) {
        string day = dayInput;
        // Normalize day input to lowercase for case-insensitive comparison
        transform(day.begin(), day.end(), day.begin(), ::tolower);

        // Map of lowercase day names to proper case
        map<string, string> dayMap = {
            {"monday", "Monday"},
            {"tuesday", "Tuesday"},
            {"wednesday", "Wednesday"},
            {"thursday", "Thursday"},
            {"friday", "Friday"}
        };

        if (dayMap.find(day) == dayMap.end()) {
            std::cout << "Invalid day: " << dayInput << std::endl;
            return;
        }
        string properDay = dayMap[day];
        std::cout << "Editing schedule for " << properDay << std::endl;

        while (true) {
            std::cout << "Current schedule for " << properDay << ":" << std::endl;
            std::cout << "Slot\t| ";
            for (const auto& classroom : CLASSROOMS) {
                std::cout << classroom << "\t| ";
            }
            std::cout << std::endl;

            for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) {
                std::cout << slot + 1 << "\t| ";
                for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
                    const auto& slotData = timetable[properDay][room][slot];
                    if (!slotData.courseName.empty()) {
                        std::cout << slotData.courseName.substr(0, 5) << " (" << slotData.instructor.substr(0, 3) << ")\t| ";
                    } else {
                        std::cout << "Free\t| ";
                    }
                }
                std::cout << std::endl;
            }

            std::cout << "Enter slot number to edit (1-" << SLOTS_PER_DAY << ", or 0 to exit): ";
            int slotNum;
            std::cin >> slotNum;
            if (slotNum == 0) {
                break;
            }
            if (slotNum < 1 || slotNum > SLOTS_PER_DAY) {
                std::cout << "Invalid slot number." << std::endl;
                continue;
            }
            int slotIndex = slotNum - 1;

            std::cout << "Enter classroom number to edit (1-" << CLASSROOMS.size() << "): ";
            int classroomNum;
            std::cin >> classroomNum;
            if (classroomNum < 1 || classroomNum > (int)CLASSROOMS.size()) {
                std::cout << "Invalid classroom number." << std::endl;
                continue;
            }
            int classroomIndex = classroomNum - 1;

            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

            std::cout << "Current slot info: ";
            const auto& currentSlot = timetable[properDay][classroomIndex][slotIndex];
            if (!currentSlot.courseName.empty()) {
                std::cout << currentSlot.courseName << " by " << currentSlot.instructor << std::endl;
            } else {
                std::cout << "Free" << std::endl;
            }

            std::cout << "Enter new course name (or leave empty to clear slot): ";
            std::string newCourseName;
            std::getline(std::cin, newCourseName);

            if (newCourseName.empty()) {
                // Clear slot
                timetable[properDay][classroomIndex][slotIndex] = Slot{};
                std::cout << "Slot cleared." << std::endl;
            } else {
                std::cout << "Enter instructor name: ";
                std::string newInstructor;
                std::getline(std::cin, newInstructor);
                newInstructor = toLowerCase(trim(newInstructor));
                if (newInstructor.empty()) {
                    std::cout << "Invalid instructor name. Slot not updated." << std::endl;
                    continue;
                }

                std::cout << "Enter speciality: ";
                std::string newSpeciality;
                std::getline(std::cin, newSpeciality);
                newSpeciality = trim(newSpeciality);
                if (newSpeciality.empty()) {
                    std::cout << "Invalid speciality. Slot not updated." << std::endl;
                    continue;
                }

                timetable[properDay][classroomIndex][slotIndex] = Slot{
                    newCourseName, newInstructor, newSpeciality, CLASSROOMS[classroomIndex], properDay, slotIndex
                };
                std::cout << "Slot updated." << std::endl;
            }
        }
    }

    void addCourse(string courseName, string instructor, string speciality, int duration, int creditHours) 
    {
        // Trim and validate inputs
        courseName = trim(courseName);
        speciality = trim(speciality);
        string instructorOriginal = trim(instructor);

        if (courseName.empty()) {
            cout << "Error: Course name cannot be empty." << endl;
            return;
        }
        if (instructorOriginal.empty()) {
            cout << "Error: Instructor name cannot be empty." << endl;
            return;
        }
        if (speciality.empty()) {
            cout << "Error: Speciality cannot be empty." << endl;
            return;
        }
        if (duration <= 0) {
            cout << "Error: Duration must be positive." << endl;
            return;
        }
        if (creditHours <= 0) {
            cout << "Error: Credit hours must be positive." << endl;
            return;
        }

        // Normalize instructor name to lowercase for consistent comparison
        string instructorLower = toLowerCase(instructorOriginal);

        // Store mapping from lowercase to original case
        instructorNameMap[instructorLower] = instructorOriginal;

        Course course = {courseName, instructorLower, speciality, duration, creditHours};
        courseTree.insertCourse(course);  //put values in AVL Tree
    }

    void deleteCourse(string courseName)
     {
        courseTree.deleteCourse(courseName);
    }

    void searchCourse(string courseName)
     {
        courseTree.searchCourse(courseName);
    }

    void displayCourses() 
    {
        vector<Course> courses;
        courseTree.getAllCourses(courses);
        for (const auto& course : courses) {
            cout << "Course Name: " << course.courseName << ", Instructor: " << course.instructor << ", Speciality: " << course.speciality << ", Duration: " << course.duration << " hours, Credit Hours: " << course.creditHours << endl;
        }
    }

    void generateTimetable(size_t startDayIndex = 0)
     {
        vector<Course> courses;
        courseTree.getAllCourses(courses);

        sort(courses.begin(), courses.end(), [](const Course& a, const Course& b) {
            return a.duration > b.duration;
        }
        );

        for (const auto& course : courses)
         {
            allocateCourse(course, startDayIndex);
        }

        detectConflicts();
        saveTimetableToFile();
    }

    void displayInstructorSchedule(const string& instructor)  //display timetable for specific instructor of complete week
    {
        string instructorLower = toLowerCase(trim(instructor));
        string displayName = instructorNameMap.count(instructorLower) ? instructorNameMap[instructorLower] : instructor;
        cout << "Schedule for Instructor: " << displayName << endl;
        for (const auto& day : DAYS) {
            cout << "Day: " << day << endl;
            for (size_t room = 0; room < CLASSROOMS.size(); ++room) 
            {
                for (int slot = 0; slot < SLOTS_PER_DAY; ++slot)
                 {
                    const auto& slotData = timetable[day][room][slot];
                    if (toLowerCase(trim(slotData.instructor)) == instructorLower)
                     {
                        cout << "  Slot " << slot + 1 << ": " << slotData.courseName << " in " << slotData.classroom << endl;
                    }
                }
            }
        }
    }

    void inputCoursesFromUser()
     {
        int numCourses;
        cout << "Enter number of courses to add: ";
        cin >> numCourses;
        for (int i = 0; i < numCourses; ++i)
         {
            string courseName, instructor, speciality;
            int duration, creditHours;

            cout << "Enter Course Name: ";

            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            getline(cin, courseName);

            cout << "Enter Instructor Name: ";
            getline(cin, instructor);
            instructor = toLowerCase(trim(instructor));

            cout << "Enter Speciality: ";
            getline(cin, speciality);

            cout << "Enter Duration (hours): ";
            while (!(cin >> duration) || duration <= 0) {
                cout << "Invalid input. Please enter a positive integer for duration: ";
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }
            cout << "Enter Credit Hours: ";
            while (!(cin >> creditHours) || creditHours <= 0) {
                cout << "Invalid input. Please enter a positive integer for credit hours: ";
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }

            addCourse(courseName, instructor, speciality, duration, creditHours);
        }
    }

    void inputCoursesFromFile(const string& filePath) {
    ifstream inFile(filePath);
    if (!inFile) {
        cerr << "Error: Unable to open file " << filePath << endl;
        return;
    }

    string courseName, instructor, speciality;
    int duration, creditHours;

    while (true) {

        if (!getline(inFile, courseName)) break; // Read course name
        courseName = trim(courseName);
        if (courseName.empty()) {
            cerr << "Error: Empty course name in file. Skipping entry." << endl;
            // Skip rest of entry
            getline(inFile, instructor);
            getline(inFile, speciality);
            inFile >> duration;
            inFile >> creditHours;
            inFile.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        if (!getline(inFile, instructor)) break;// Read instructor name
        instructor = toLowerCase(trim(instructor));
        if (instructor.empty()) {
            cerr << "Error: Empty instructor name in file. Skipping entry." << endl;
            getline(inFile, speciality);
            inFile >> duration;
            inFile >> creditHours;
            inFile.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        if (!getline(inFile, speciality)) break; // Read speciality
        speciality = trim(speciality);
        if (speciality.empty()) {
            cerr << "Error: Empty speciality in file. Skipping entry." << endl;
            inFile >> duration;
            inFile >> creditHours;
            inFile.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        if (!(inFile >> duration)) break; // Read duration
        if (duration <= 0) {
            cerr << "Error: Invalid duration in file. Skipping entry." << endl;
            inFile >> creditHours;
            inFile.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        if (!(inFile >> creditHours)) break; // Read credit hours
        if (creditHours <= 0) {
            cerr << "Error: Invalid credit hours in file. Skipping entry." << endl;
            inFile.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        inFile.ignore(numeric_limits<streamsize>::max(), '\n'); // Clear the spacing

        Course course = {courseName, instructor, speciality, duration, creditHours};

        addCourse(course.courseName, course.instructor, course.speciality, course.duration, course.creditHours);

        cout << "Loaded Course: " << course.courseName << " by " << course.instructor 
             << " (" << course.speciality << "), Duration: " << course.duration 
             << ", Credit Hours: " << course.creditHours << endl; // Debug log
    }

    inFile.close();
    cout << "Courses successfully loaded from file." << endl;
    }

    void displayTimetable()
     {
        cout << "============================== Timetable ==============================" << endl;
        for (const auto& day : DAYS)
         {
            cout << "Day: " << day << endl;
            cout << "-----------------------------------------------------------------------" << endl;
            cout << "Slot\t| ";

            for (const auto& classroom : CLASSROOMS)
             {
                cout << classroom << "\t| ";
            }
            cout << "\n-----------------------------------------------------------------------" << endl;

            for (int slot = 0; slot < SLOTS_PER_DAY; ++slot) {

                cout << "Slot " << slot + 1 << "\t| ";

                for (size_t room = 0; room < CLASSROOMS.size(); ++room) {
                    const auto& slotData = timetable[day][room][slot];

                    if (!slotData.courseName.empty()) 
                    {
                        cout << slotData.courseName.substr(0, 5) << " (" << slotData.instructor.substr(0, 3) << ")\t| ";
                    } else {
                        cout << "Free\t| ";
                    }
                }
                cout << "\n";
            }
            cout << "=======================================================================" << endl;
        }
    }
};


int main() {
    Scheduler scheduler;

    std::string filePath = "courses_info.txt";

    scheduler.inputCoursesFromFile(filePath);

    scheduler.displayCourses();

    std::cout << "Enter starting day for schedule allocation (0=Monday, 1=Tuesday, ..., 4=Friday): ";
    int startDayInput;
    while (!(std::cin >> startDayInput) || startDayInput < 0 || startDayInput >= (int)DAYS.size()) {
        std::cout << "Invalid input. Please enter a number between 0 and " << (int)DAYS.size() - 1 << ": ";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    scheduler.generateTimetable(static_cast<size_t>(startDayInput));

    scheduler.displayTimetable();

    while (true) {
        std::cout << "Options:\n1. View instructor schedule\n2. Edit schedule for a day\n3. Show full timetable\n4. Exit\n5. Clear schedule for a day\n6. Clear schedule for all days\nEnter choice: ";
        int choice;
        if (!(std::cin >> choice)) {
            std::cout << "Invalid input. Please enter a number between 1 and 6." << std::endl;
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (choice == 1) {
            std::string instructor;
            std::cout << "Enter instructor name: ";
            std::getline(std::cin, instructor);
            scheduler.displayInstructorSchedule(instructor);
        } else if (choice == 2) {
            std::string day;
            std::cout << "Enter day to edit (e.g., Monday): ";
            std::getline(std::cin, day);
            scheduler.editScheduleForDay(day);
        } else if (choice == 3) {
            std::cout << "Displaying full timetable:" << std::endl;
            scheduler.displayTimetable();
        } else if (choice == 4) {
            std::cout << "Exiting program. Here is the full created timetable:" << std::endl;
            scheduler.displayTimetable();
            break;
        } else if (choice == 5) {
            std::string day;
            std::cout << "Enter day to clear schedule (e.g., Monday): ";
            std::getline(std::cin, day);
            scheduler.clearScheduleForDay(day);
        } else if (choice == 6) {
            scheduler.clearScheduleForAllDays();
        } else {
            std::cout << "Invalid choice. Please enter a number between 1 and 6." << std::endl;
        }
    }

    return 0;
}


```


## Milestone 3

### Optimization and Efficiency Analysis

Below is a table of comparison of algorithms used in our code versus algorithms that could have been used instead. The pros and cons of each of the algorithms were compared and finally an algorithm was chosen to be implemented in the code.

#### AVL Trees vs Alternatives

| Feature            | **Current: AVL Tree**                        | **Alternatives**                             | **Comparison**                                                                                          |
| ------------------ | -------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Fast Insert/Search | O(log n) using balanced BST                  | Red-Black Tree, Hash Table                   | Red-Black: fewer rotations, slightly faster insertions; Hash Table: O(1) average lookup but no ordering |
| Ordered Traversal  | Yes (via in-order traversal)                 | Hash Table: ❌, Red-Black Tree: ✅             | AVL is ideal if ordered data output is required                                                         |
| Space Efficiency   | Moderate (pointers + balance factor)         | Similar (RB), Hash Table may use more memory | Balanced trees trade a bit of space for speed                                                           |
| Best Use Case      | When you need **sorted** data + fast lookups | Hash Table for unordered rapid access        | ✅ AVL is a strong balanced option for your use case                                                     |

#### Linked List vs Alternatives

| Feature               | **Current: Linked List**       | **Alternatives**                        | **Comparison**                                       |
| --------------------- | ------------------------------ | --------------------------------------- | ---------------------------------------------------- |
| Insertion Flexibility | Easy to insert anywhere (O(n)) | Dynamic Array: O(n), Doubly LL: similar | Linked List is good for dynamic, unpredictable sizes |
| Access Speed          | O(n) to access middle elements | Dynamic Array: O(1) random access       | Arrays win in static data use cases                  |
| Memory Overhead       | High (due to pointers)         | Arrays are more compact                 | LL uses more memory per element                      |
| Best Use Case         | Variable-length schedules      | Array: fixed schedules                  | ✅ Linked list is flexible for per-day lecture lists  |


#### Maps vs Alternatives

| Feature         | `std::map` (Used)         | `unordered_map`                      |
| --------------- | ------------------------- | ------------------------------------ |
| Time Complexity | O(log n)                  | O(1) average, O(n) worst-case        |
| Ordering        | ✅ Ordered by key          | ❌ Unordered                          |
| Use-case Fit    | Needed for sorted outputs | Better if you only need fast lookups |


### Edge Case Testing


<img width="655" alt="Screenshot 2025-05-04 at 1 14 24 AM" src="https://github.com/user-attachments/assets/8f604eab-716f-4871-8724-c3bd97889326" />


<img width="696" alt="Screenshot 2025-05-04 at 1 14 05 AM" src="https://github.com/user-attachments/assets/2ac1f1ee-eeb2-4860-9f10-c7882c121ac3" />


<img width="655" alt="Screenshot 2025-05-04 at 1 14 24 AM" src="https://github.com/user-attachments/assets/d7988ba1-a0e0-4d75-8794-a04045934c4a" />


<img width="528" alt="Screenshot 2025-05-04 at 1 14 40 AM" src="https://github.com/user-attachments/assets/ea8a282a-380a-4aa5-bbf6-f0f80962d386" />


<img width="457" alt="Screenshot 2025-05-04 at 1 15 03 AM" src="https://github.com/user-attachments/assets/029ea27d-14bc-4550-b3bf-f4b252d50a36" />



