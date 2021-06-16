document.body.onload= () => {
	const focusedIngredients = document.getElementsByClassName('focused');
	for (let label of focusedIngredients) {
	    label.lastElementChild.checked = true;
	}
}


const ingredientsForm = document.getElementById('choices');

ingredientsForm.onclick = () => {
	console.log(3);
	event.preventDefault();
	const target = event.target;
	if (target.parentElement.tagName == 'LABEL') {   
		console.log(1);
		target.parentElement.classList.toggle('focused');
 		target.parentElement.lastElementChild.checked = (target.parentElement.lastElementChild.checked) ? false : true;
	} else if (event.target.tagName == 'LABEL') {
		console.log(2);
    	target.classList.toggle('focused');
    	target.lastElementChild.checked = (target.parentElement.lastElementChild.checked) ? false : true;
	}
};