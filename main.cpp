#include <iostream>
#include <cstdio>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>
#include "pctMileMarkers.cpp"
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

    //getting coords of start and finish
    string startCoordsLat;
    string startCoordsLon;
    string finishCoordsLat;
    string finishCoordsLon;
    startCoordsLat=to_string(coordsFuncLat(startMile));
    startCoordsLon=to_string(coordsFuncLon(startMile));
    finishCoordsLat=to_string(coordsFuncLat(finishMile));
    finishCoordsLon=to_string(coordsFuncLon(finishMile));



    //editing gpx file
    string full;
    string checker = "/ele";
    int count = 0;
    int countStart=0;
    int countFinish=0;

    //get line number for start and finish
    myFile.open("pct500.gpx", ios::in);
    if (myFile.is_open()){
        string data;
        while (getline(myFile, data)) {
            size_t findLat = data.find(startCoordsLat.substr(0,6));
            size_t findLon = data.find(startCoordsLon.substr(0,7));
            if (findLat!=std::string::npos && findLon!=std::string::npos){
                    cout<<"found\n";
                    cout<<startCoordsLat<<" is start coords Lat\n";
                    cout<<startCoordsLon<<" is start coords Lon\n";
                    cout<<data<<" is data\n\n\n";
                    break;
                }
                countStart++;
        }
    }
    myFile.close();


    myFile.open("pct500.gpx", ios::in);
    if (myFile.is_open()){
        string data;
        while (getline(myFile, data)) {
            size_t findLat2 = data.find(finishCoordsLat.substr(0,6));
            size_t findLon2 = data.find(finishCoordsLon.substr(0,8));
            if (findLat2!=std::string::npos && findLon2!=std::string::npos){
                    cout<<"found\n";
                    cout<<finishCoordsLat<<" is finish coords Lat\n";
                    cout<<finishCoordsLon<<" is finish coords Lon\n";
                    cout<<data<<" is data\n\n\n";
                    break;
                }
                countFinish++;
        }
    }
    myFile.close();



    //change these to pinpoints lat lon coords
    //change theseto pinpoints lat lon coords
    string front;

    int   var_start = countStart-1;
    int   var_fin = countFinish+15;

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
