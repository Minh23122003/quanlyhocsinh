let quantity_student = 0
let quantity_student_in_class = 0
id_class = 0

function changeClass() {
    fetch("/api/changeClass", {
        method: "post",
        body: JSON.stringify({
            "id_student" : document.getElementById('id_student').value,
            "id_class" : document.getElementById('id_class').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        document.getElementById('btn_changeClass').blur()
        let a = document.getElementById('changeClass')
        if(data.content === "Thành công")
            a.innerHTML = `<div class="alert alert-success">${data.content}</div>`
        else
            a.innerHTML = `<div class="alert alert-danger">${data.content}</div>`
    });
}

function searchStudent() {
    fetch("/api/searchStudent", {
        method: "post",
        body: JSON.stringify({
            "searchstudent" : document.getElementById('searchstudent').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        if (data[0].quantity === 0)
        {
            let a = document.getElementById('no_result_searchstudent')
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-success">Không tìm thấy học sinh</div>`
            let b = document.getElementById('result_searchstudent')
            b.style.display = "none"
        }
        else
        {
            let b = document.getElementById('no_result_searchstudent')
            b.style.display = "none"
            let a = document.getElementById('result_searchstudent')
            a.style.display = "inline"
            let table = document.getElementById('table_result')

            for (let j =1; j <= quantity_student; j++)
                table.deleteRow(1)

            quantity_student = data[0].quantity

            for (let j = 1; j <= data[0].quantity; j++)
            {
                var row = table.insertRow()
                row.insertCell().innerText = data[j].id
                row.insertCell().innerText = data[j].name
                row.insertCell().innerText = data[j].class
            }
        }

    });
}

function printClass(id) {
    fetch("/api/printClass", {
        method: "post",
        body: JSON.stringify({
            "id_class" : id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let id = document.getElementById(data[0].id)
        id.classList.add("active")
        if (id_class != 0)
        {
            let id_remove = document.getElementById(id_class)
            id_remove.classList.remove("active")
        }

        id_class = data[0].id
        let a = document.getElementById('no_student')
        let b = document.getElementById('print_class')
        if(data[0].quantity == 0)
        {
            a.style.display = "inline"
            a.innerHTML = `<div class="alert alert-info text-center">Lớp không có học sinh</div>`
            b.style.display = "none"
        }
        else
        {
            let name_class = document.getElementById('name_class')
            name_class.innerText = `Lớp: ${data[0].class}`
            let quantity = document.getElementById('quantity')
            quantity.innerText = `Sĩ số: ${data[0].quantity}`

            a.style.display = "none"
            b.style.display = "inline"
            let table = document.getElementById('table_print_class')

            for(let i = 1; i <= quantity_student_in_class; i++)
                table.deleteRow(1)

            quantity_student_in_class = data[0].quantity

            for(let i = 1; i <= data[0].quantity; i++)
            {
                var row = table.insertRow()
                row.insertCell().innerText = i
                row.insertCell().innerText = data[i].name
                row.insertCell().innerText = data[i].sex
                row.insertCell().innerText = data[i].DoB
                row.insertCell().innerText = data[i].address
            }
        }
    });
}

function printClassPrevious(){
    if (id_class == 0)
        printClass(15)
    else if (id_class == 1)
        printClass(15)
    else
        printClass(id_class - 1)
}

function printClassNext(){
    if (id_class == 0)
        printClass(1)
    else if (id_class == 15)
        printClass(1)
    else
        printClass(id_class + 1)
}
