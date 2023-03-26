#include <iostream>
#include <cstdio>
#include <string>
#include <fstream>
#include <sstream>
using namespace std;

int main() {
    float startMile;
    float finishMile;
    char year[100];
    string year1;
    char month[100];
    string month1;
    char day[100];
    string day1;
    string time = "08:00:00Z</time>\n";
    string fullTime;
    ofstream newFile;
    fstream myFile;

    cout<<"enter start mile: \n";
    // get starting mileage for the day
    scanf("%f", &startMile);
    cout<<"starting mile is " << startMile << "\n";

    cout<<"enter finish mile: \n";
    // get finishing mileage for the day
    scanf("%f", &finishMile);
    cout<<"finishing mile is " << finishMile << "\n";

    //totl mileage on said day
    cout<<"total day mileage = " << finishMile-startMile << "\n";


    cout<<"enter the year in xxxx format: \n";
    // getting year
    scanf("%100s", &year);
    year1=year;
    cout<<"year is " << year1 << "\n";

    cout<<"enter the month in x format: \n";
    // getting month
    scanf("%100s", &month);
    month1=month;
    cout<<"month is " << month1 << "\n";

    cout<<"enter the day in xx format: \n";
    // getting day
    scanf("%100s", &day);
    day1=day;
    cout<<"day is " << day1 << "\n";

    fullTime="<time>"+year1+"-"+month1+"-"+day1+"T"+time;
    cout<<fullTime;



    //editing gpx file
    string full;
    string checker = "/ele";
    int count = 0;
    float starting = startMile*245+17;
    cout<<to_string(starting)+"\n";
    float finishing = finishMile*245+19;
    cout<<to_string(finishing)+"\n";
    string front;

    int   var_start = (int)starting;
    int   var_fin = (int)finishing;

    myFile.open("pct500.gpx", ios::in);
    if (myFile.is_open()) {
        string data;
        while (getline(myFile, data)) {
            if(count<19){
                front=front+data+"\n";
            }
            else if(var_start<count && count<var_fin){
                // cout<<"start is "<<var_start<<"   fin is "<<var_fin<<"   c ount is "<<count;
                full=full+data+"\n";
                size_t found = data.find(checker);
                if (found!=std::string::npos){
                    full=full+fullTime;
                }
            }
            else if(count>88293){
                full=full+data+"\n";
            }
            count++;
        }
        myFile.close();
    }
    full=front+full;
    newFile.open("newFile1.gpx", ios::out);
    if(newFile.is_open()){
        newFile<<full;
    }
    newFile.close();

}
