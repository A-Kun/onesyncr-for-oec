window.onload = function(){
	// get all li tags
	var lis = document.getElementsByTagName('li');

	// looping through all  li tags listen click event
	for(var i = 0; i<lis.length; i++){
		lis[i].onclick = function(){
			startShow(this);
		}
	}
}

function startShow(obj){
	// get target element
	var target = document.getElementById('main_content_wrap');
	if(obj.innerHTML == "Home"){
		target.innerHTML = '<object type="text/html" data="home.html" ></object>';
	}else if(obj.innerHTML == "Contact"){
		target.innerHTML='<object type="text/html" data="contact.html" ></object>';
	}else if(obj.innerHTML == "News"){
		target.innerHTML='<object type="text/html" data="news.html" ></object>';
	}else if(obj.innerHTML == "Deliverable #2"){
		target.innerHTML='<object type="text/html" data="d2.html" ></object>';
	}else if(obj.innerHTML == "Deliverable #3 part 1"){
		target.innerHTML='<object type="text/html" data="d3p1.html" ></object>';
	}
}
