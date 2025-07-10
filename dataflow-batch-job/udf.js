function transform(line) {
    var values = line.split(',');
    if (values[0] == "EmployeeID") {
        return null; // Skip header row
    }
    // create object mapping the values to the BigQuery schema 
    // EmployeeID,FirstName,LastName,Department,Position,Salary,JoiningDate,Country
    var obj = new Object();
    obj.EmployeeID = parseInt(values[0]);
    obj.FirstName = values[1];
    obj.LastName = values[2];
    obj.Department = values[3];
    obj.Position = values[4];
    obj.Salary = parseFloat(values[5]);
    obj.JoiningDate = new Date(values[6]);
    obj.Country = values[7];
    var jsonString = JSON.stringify(obj);
    // return the JSON string   
    return jsonString;
}
