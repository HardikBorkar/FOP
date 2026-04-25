#include <stdio.h>
#include <string.h>
#include "logic.h"

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

// Add shelter
int addshelter(int id, const char* name, const char* location, int cap, int food, int water, int med, int ad) {
    FILE *fptr = fopen("Shelter.txt", "a");
    if (!fptr) return 0;
    fprintf(fptr, "%d||%s||%s||%d||%d||%d||%d||%d\n", id, name, location, cap, food, water, med, ad);
    fclose(fptr);
    return 1;
}

// View all shelters
void viewshelters() {

    FILE *fptr = fopen("Shelter.txt", "r");

    if (!fptr) {
        printf("No shelter records found!\n");
        return;
    }

    int id, cap, food, water, med, ad;
    char name[100], location[100];

    printf("\n=============================================\n");
    printf("           LIST OF ALL SHELTERS\n");
    printf("=============================================\n\n");

    while (fscanf(fptr,
        "%d||%99[^|]||%99[^|]||%d||%d||%d||%d||%d\n",
        &id,
        name,
        location,
        &cap,
        &food,
        &water,
        &med,
        &ad) != EOF)
    {
        printf("🆔 Shelter ID     : %d\n", id);
        printf("🏷️ Name           : %s\n", name);
        printf("📍 Location       : %s\n", location);
        printf("👥 Capacity       : %d\n", cap);
        printf("🏠 Admitted       : %d\n", ad);
        printf("🍞 Food Units     : %d\n", food);
        printf("💧 Water Units    : %d\n", water);
        printf("💊 Medical Kits   : %d\n", med);
        printf("---------------------------------------------\n");
    }

    fclose(fptr);
}

// Admit people
int admit(int id, int n) {
    FILE *fptr = fopen("Shelter.txt", "r");
    FILE *temp = fopen("temp.txt", "w");
    if(!fptr || !temp) return 0;
    struct shelter s;
    int flag = 0;
    while(fscanf(fptr, "%d||%99[^|]||%99[^|]||%d||%d||%d||%d||%d\n",
                 &s.id, s.name, s.location, &s.cap, &s.food, &s.water, &s.med, &s.ad) != EOF) {
        if(s.id == id) {
            if(s.ad + n <= s.cap) s.ad += n;
            else { fclose(fptr); fclose(temp); return -1; } // Not enough capacity
            flag = 1;
        }
        fprintf(temp,"%d||%s||%s||%d||%d||%d||%d||%d\n",
                s.id,s.name,s.location,s.cap,s.food,s.water,s.med,s.ad);
    }
    fclose(fptr); fclose(temp);
    remove("Shelter.txt");
    rename("temp.txt","Shelter.txt");
    return flag;
}

// Restock
int restock(int id, int food, int water, int med) {
    FILE *fptr = fopen("Shelter.txt", "r");
    FILE *temp = fopen("temp.txt", "w");
    if(!fptr || !temp) return 0;
    struct shelter s; int found = 0;
    while(fscanf(fptr, "%d||%99[^|]||%99[^|]||%d||%d||%d||%d||%d\n",
                 &s.id, s.name, s.location, &s.cap, &s.food, &s.water, &s.med, &s.ad) != EOF) {
        if(s.id == id) { s.food += food; s.water += water; s.med += med; found = 1; }
        fprintf(temp,"%d||%s||%s||%d||%d||%d||%d||%d\n",
                s.id,s.name,s.location,s.cap,s.food,s.water,s.med,s.ad);
    }
    fclose(fptr); fclose(temp);
    remove("Shelter.txt"); rename("temp.txt","Shelter.txt");
    return found;
}

// Transfer
int transfer(int fromID, int toID, int food, int water, int med) {
    FILE *fptr = fopen("Shelter.txt", "r");
    FILE *temp = fopen("temp.txt", "w");
    if(!fptr || !temp) return 0;
    struct shelter s;
    while(fscanf(fptr, "%d||%99[^|]||%99[^|]||%d||%d||%d||%d||%d\n",
                 &s.id, s.name, s.location, &s.cap, &s.food, &s.water, &s.med, &s.ad) != EOF) {
        if(s.id == fromID) { s.food -= food; s.water -= water; s.med -= med; }
        if(s.id == toID) { s.food += food; s.water += water; s.med += med; }
        fprintf(temp,"%d||%s||%s||%d||%d||%d||%d||%d\n",
                s.id,s.name,s.location,s.cap,s.food,s.water,s.med,s.ad);
    }
    fclose(fptr); fclose(temp);
    remove("Shelter.txt"); rename("temp.txt","Shelter.txt");
    return 1;
}

// Shortage 
int shortage(int* ids, int* food_short, int* water_short, int* med_short) {
    FILE *fptr = fopen("Shelter.txt", "r");
    if(!fptr) return 0;

    struct shelter s;
    int count = 0;

    while (fscanf(fptr, "%d||%99[^|]||%99[^|]||%d||%d||%d||%d||%d\n",
                 &s.id, s.name, s.location, &s.cap, &s.food, &s.water, &s.med, &s.ad) ==8)
{
    int f_short = 0, w_short = 0, m_short = 0;

    if (s.food < s.cap * 2)
        f_short = (s.cap * 2) - s.food;

    if (s.water < s.cap * 3)
        w_short = (s.cap * 3) - s.water;

    if (s.med < s.cap)
        m_short = s.cap - s.med;

    if (f_short > 0 || w_short > 0 || m_short > 0)
    {
        ids[count] = s.id;
        food_short[count] = f_short;
        water_short[count] = w_short;
        med_short[count] = m_short;
        count++;
    }
}

    fclose(fptr);
    return count;
}
