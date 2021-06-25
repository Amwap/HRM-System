var user
var panel = null
var pageCount = 0
var opened_table

request = function(form){
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        commits = x.response
        panel = x.response
        var panelField = document.getElementsByClassName('feature_box')
        panelField.innerHTML = panel
    }
    x.send(null);
}

function setPanel(){
    var form = `?&login=${user}&element=panel`
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        var div = document.createElement('div')
        div.innerHTML = x.response
        document.querySelector('div.table_box').innerHTML = ''
        document.querySelector('div.feature_box').appendChild(div)
    }
    x.send(null);
}

function setMainTable(name, sorted=''){
    var form = `?&login=${user}&element=${name}&sorted=${sorted}`
    opened_table = name
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        var div = document.createElement('div')
        div.innerHTML = x.response
        document.querySelector('div.table_box').innerHTML = ''
        document.querySelector('div.table_box').appendChild(div)
    }
    x.send(null);
}


function onload(){
    user = window.location.search.substr(1).split('=')[1]
    setPanel()
    setMainTable('groupsTable')
    console.log(user)
}

function loadChecker(){
    console.log(user)
}

function sendRequest(form){
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        alert(x.response)
    }
    x.send(null);
}

function search(form){
    form = `?&login=${user}`+
    `&element=searchQuery`+
    `&data=${form.searchField.value}`+
    `&subelement=${opened_table}`

    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        var div = document.createElement('div')
        div.innerHTML = x.response
        document.querySelector('div.table_box').innerHTML = ''
        document.querySelector('div.table_box').appendChild(div)
    }
    x.send(null);

    return false
}

function checkRightPart(event){
    if (event == 'open'){ pageCount += 1 }
    else if (event == 'close'){ pageCount -= 1 }
    if (pageCount <= 0){
        pageCount = 0
        document.querySelector('div.right_part').style.display = 'none'
    }
    else if (pageCount > 0){
        document.querySelector('div.right_part').style.display = 'flex'
    }
    console.log(pageCount)
}


function openPage(name=0){
    var form = `?&login=${user}&element=${name}`
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        var div = document.createElement('div')
        checkRightPart('open')
        div.id = `pageid${pageCount}`
        div.innerHTML = x.response
        document.querySelector('div.right_part').appendChild(div)
    }
    x.send(null);
}


function closePage(){
    console.log(document.querySelector(`div#pageid${pageCount}`).remove())
    checkRightPart('close')
}


function sendRequest(form){
    var x = new XMLHttpRequest();
    x.open("GET", 'api'+form, true);
    x.onload = function (){
        alert(x.response)
    }
    x.send(null);
}

function requestOnDelete(query){
    var conf = confirm('Подтвердите запрос на удаление')
    if (conf){ 
        form = `?&login=${user}&element=${query}`
        var x = new XMLHttpRequest();
        x.open("GET", 'api'+form, true);
        x.onload = function (){
            alert(x.response)
        }
        x.send(null);
    }
}

function exit() {
    var data = `?&login=${user}&element=exit&exit=out`
    var x = new XMLHttpRequest();
        x.open("GET", "api"+data, true);
        x.onload = function (){
            window.location.href = "/"
         }
        x.send(null);
    return false;
  }

function sendGroupForm(form) {
    console.log(form.leader.value)
    var data = `?&login=${user}`+
    `&element=createGroup`+
    `&group_id=${form.id.value}`+
    `&name=${form.name.value}`+
    `&year=${form.year.value}`+
    `&leader=${form.leader.value}`
    sendRequest(data)
    return false;
  }

function sendParentForm(form) {
    var data = `?&login=${user}`+
    `&element=createParent`+
    `&parent_id=${form.parent_id.value}`+
    `&student_id=${form.student_id.value}`+
    `&name=${form.name.value}`+
    `&surename=${form.surename.value}`+
    `&patronymic=${form.patronymic.value}`+
    `&phone=${form.phone.value}`+
    `&email=${form.email.value}`+
    `&who=${form.who.value}`+
    `&note=${form.note.value}`
    sendRequest(data)
    return false;
  }

function sendStuffForm(form) {
    var data = `?&login=${user}`+
    `&element=createStuff`+
    `&stuff_id=${form.id.value}`+
    `&name=${form.name.value}`+
    `&surename=${form.surename.value}`+
    `&patronymic=${form.patronymic.value}`+
    `&phone=${form.phone.value}`+
    `&email=${form.email.value}`+
    `&note=${form.note.value}`+
    `&admin=${form.admin.value}`+
    `&specialist=${form.specialist.value}`+
    `&login=${form.login.value}`+
    `&password=${form.password.value}`
    sendRequest(data)
    return false;
  }


function sendStudentForm(form) {
    second_form = document.querySelector('form.additional_form')

    var data = `?&login=${user}`+
    `&element=createStudent`+
    `&student_id=${form.student_id.value}`+
    `&name=${form.name.value}`+
    `&surename=${form.surename.value}`+
    `&patronymic=${form.patronymic.value}`+
    `&email=${form.email.value}`+
    `&phone=${form.phone.value}`+
    `&note=${second_form.note.value}`+
    `&group=${second_form.group.value}`+
    `&parentsArePensioners=${second_form.parentsArePensioners.value}`+
    `&amountOfChildren=${second_form.amountOfChildren.value}`+
    `&dateOfBirth=${form.dateOfBirth.value}`+
    `&cityOfRegistration=${form.cityOfRegistration.value}`+
    `&cityOfResidence=${form.cityOfResidence.value}`+
    `&gender=${form.gender.value}`+
    `&juvenileAffairsUnit=${second_form.juvenileAffairsUnit.value}`+
    `&fullFamily=${second_form.fullFamily.value}`+
    `&interests=${second_form.interests.value}`+
    `&sportsSections=${second_form.sportsSections.value}`
    sendRequest(data)
    return false;
  }


function open_page(id){
    // Открывает страницы из таблиц lead-

    var element = id.split("-")[0]
    var element_id = id.split("-")[1]
    if (element_id == ''){ return }

    var query = `${element}&element_id=${element_id}`
    openPage(query)
}

function get_sorted(parm){
    setMainTable(opened_table, parm)
}