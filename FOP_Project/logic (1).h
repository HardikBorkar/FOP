#ifndef LOGIC_H
#define LOGIC_H

// Struct definition
struct shelter {
    int id;
    char name[100];
    char location[100];
    int cap;
    int food;
    int water;
    int med;
    int ad;
};

// Function prototypes

// Add shelter
int addshelter(int id, const char* name, const char* location, int cap, int food, int water, int med, int ad);

// View all shelters
void viewshelters();

// Admit people
int admit(int id, int n);

// Check shortage
int shortage(int* ids, int* food_short, int* water_short, int* med_short);

// Restock shelter resources
int restock(int id, int food, int water, int med);

// Transfer resources between shelters
int transfer(int fromID, int toID, int food, int water, int med);

#endif