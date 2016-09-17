window.onload = function(){
	// get all li tags
	var lis = document.getElementsByTagName('li');

	// get target element
	var target = document.getElementById('main_content_wrap');

	// looping through all  li tags listen click event
	for(var i = 0; i<lis.length; i++){
		lis[i].onclick = function(){
			startShow(this);
		}
	}

}

function startShow(obj){
	alert(this.name);
	console.log(this.name);

}