package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"
)


type Data struct{
	Data1 string `json:"x1"`
	Data2 string `json:"x2"`
	Data3 string `json:"x3"`
	Data4 string `json:"x4"`
	Data5 string `json:"x5"`
	Data6 string `json:"x6"`
	Data7 string `json:"x7"`
	Data8 string `json:"x8"`
	Data9 string `json:"x9"`
	Data10 string `json:"x10"`
	Data11 string `json:"x11"`
	Data12 string `json:"x12"`
	Data13 string `json:"x13"`
	Data14 string `json:"x14"`
	Class string `json:"Class"`
}

type Model struct {
	Name       	string `json:"Name"`
	Parameters 	[]float64 `json:"Parameters"`
	Owner      	string `json:"Owner"`
	ObjectType  string `json:"ObjectType"`
}

type DataWrapper struct{
	Key string `json:"Key"`
	Record Data `json:"Record"`
}

type ModelWrapper struct{
	Key   string `json:"Key"`
	Record Model `json:"Record"`
}

type Results struct{
	ArrayOfResults     []float64 `json:"Results"`
	ArrayOfResultsMany [][]float64  `json:"ManyResults"`
}

type Payload struct {
	Data []byte     `json:"Data"`
	Model []byte    `json:"Model"`
}

var validationResults *Results = &Results{}
//HTTP handlers getting GET and POST methods

func validateHandler(w http.ResponseWriter, r *http.Request) {

	switch r.Method {
	case "POST":

		var payload Payload
		var fullDataStorage []DataWrapper
		var modelStorage Model
		var results Results

		// Payload parsing part
		d := json.NewDecoder(r.Body)

		err := d.Decode(&payload)
		if err != nil {
			log.Fatal(err)
		}

		json.Unmarshal(payload.Data, &fullDataStorage)
		json.Unmarshal(payload.Model, &modelStorage)

		// Model calculation part
		var arrayOfResults []float64

		model :=  modelStorage
		data := fullDataStorage


		for i := 0; i < len(data); i++ {
			result := calculateLogisticModelResults(data[i], model)
			arrayOfResults = append(arrayOfResults, result)
		}

		results.ArrayOfResults = arrayOfResults
		json, _ := json.Marshal(results)
		w.Write(json)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		fmt.Fprintf(w, "I can't do that.")
	}

}

// method for testing all models that exists in blockchain state database
func validateManyHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		var results Results
		var payload Payload
		var fullDataStorage []DataWrapper
		var fullModelStorage []ModelWrapper

		// Payload parsing part
		d := json.NewDecoder(r.Body)

		err := d.Decode(&payload)
		if err != nil {
			log.Fatal(err)
		}

		json.Unmarshal(payload.Data, &fullDataStorage)
		json.Unmarshal(payload.Model, &fullModelStorage)

		var tempArrayOfResults []float64
		var fullResults [][]float64

		for i := 0; i < len(fullModelStorage); i++ {
			model := fullModelStorage[i].Record
			tempArrayOfResults = []float64{}
			data := fullDataStorage
			for j := 0; j < len(data); j++ {
				result := calculateLogisticModelResults(data[j], model)
				tempArrayOfResults = append(tempArrayOfResults, result)
			}
			fullResults  = append(fullResults,tempArrayOfResults)
		}
		results.ArrayOfResultsMany = fullResults

		json, _ := json.Marshal(results)
		w.Write(json)


	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		fmt.Fprintf(w, "I can't do that.")
	}
}

//calculation of logistic regression results
func calculateLogisticModelResults(data DataWrapper, currentModel Model ) float64{
	var Data1 float64
	var Data2 float64
	var Data3 float64
	var Data4 float64
	var Data5 float64
	var Data6 float64
	var Data7 float64
	var Data8 float64
	var Data9 float64
	var Data10 float64
	var Data11 float64
	var Data12 float64
	var Data13 float64
	var Data14 float64

	Data1, _= strconv.ParseFloat(data.Record.Data1,64)
	Data2, _= strconv.ParseFloat(data.Record.Data2,64)
	Data3, _= strconv.ParseFloat(data.Record.Data1,64)
	Data4, _= strconv.ParseFloat(data.Record.Data2,64)
	Data5, _= strconv.ParseFloat(data.Record.Data1,64)
	Data6, _= strconv.ParseFloat(data.Record.Data2,64)
	Data7, _= strconv.ParseFloat(data.Record.Data1,64)
	Data8, _= strconv.ParseFloat(data.Record.Data2,64)
	Data9, _= strconv.ParseFloat(data.Record.Data1,64)
	Data10, _= strconv.ParseFloat(data.Record.Data2,64)
	Data11, _= strconv.ParseFloat(data.Record.Data1,64)
	Data12, _= strconv.ParseFloat(data.Record.Data2,64)
	Data13, _= strconv.ParseFloat(data.Record.Data1,64)
	Data14, _= strconv.ParseFloat(data.Record.Data2,64)

	sum:= currentModel.Parameters[0]
	sum += Data1 * currentModel.Parameters[1]
	sum += Data2 * currentModel.Parameters[2]
	sum += Data3 * currentModel.Parameters[3]
	sum += Data4 * currentModel.Parameters[4]
	sum += Data5 * currentModel.Parameters[5]
	sum += Data6 * currentModel.Parameters[6]
	sum += Data7 * currentModel.Parameters[7]
	sum += Data8 * currentModel.Parameters[8]
	sum += Data9 * currentModel.Parameters[9]
	sum += Data10 * currentModel.Parameters[10]
	sum += Data11 * currentModel.Parameters[11]
	sum += Data12 * currentModel.Parameters[12]
	sum += Data13 * currentModel.Parameters[13]
	sum += Data14 * currentModel.Parameters[14]

	result := 1 / (1 + math.Exp(-sum))

	return result
}

//Main function that runs on startup
func main() {
	srv := &http.Server{
		Addr:           ":8081",
		ReadTimeout: 600 * time.Second,
		WriteTimeout: 600 * time.Second,

	}

	http.HandleFunc("/apiValidate", validateHandler)
	http.HandleFunc("/apiValidateMany", validateManyHandler)
	log.Println("Oracle service is running!")
	log.Fatal(srv.ListenAndServe())

}