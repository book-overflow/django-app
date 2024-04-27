var sale_check = document.getElementById('id_for_sale');
var rent_check = document.getElementById('id_for_rent');

sale_check.addEventListener('change', function() {
    if (this.checked) {
        document.getElementById('checkbox-warning').style.display= 'none';
        document.getElementById('submit-button').removeAttribute('disabled');

        document.getElementById('div_id_sale_price').style.display = 'block';
        document.getElementById('id_sale_price').setAttribute('required', true);
        document.getElementById('id_sale_price').removeAttribute('disabled');
    } else {
        document.getElementById('div_id_sale_price').style.display = 'none';
        document.getElementById('id_sale_price').removeAttribute('required');
        document.getElementById('id_sale_price').setAttribute('disabled', '');
        // Show error if both checkboxes are unchecked
        if (!rent_check.checked){
            document.getElementById('checkbox-warning').style.display= 'inline';
            document.getElementById('submit-button').setAttribute('disabled',true);
        }
    }
});

rent_check.addEventListener('change', function() {
    var for_rent = document.getElementsByClassName('row-for-rent');
    var input_for_rent = document.getElementsByClassName('input-for-rent');
    if (this.checked) {
        document.getElementById('checkbox-warning').style.display= 'none';
        document.getElementById('submit-button').removeAttribute('disabled');
        for (var i = 0; i < for_rent.length; i++){
            for_rent[i].style.display = 'table-row';
        }
        for (var i = 0; i < input_for_rent.length; i++){
            input_for_rent[i].setAttribute('required', true);
            input_for_rent[i].removeAttribute('disabled');
        }
    } else {
        for (var i = 0; i < for_rent.length; i++){
            for_rent[i].style.display = 'none';
        }
        for (var i = 0; i < input_for_rent.length; i++){
            input_for_rent[i].removeAttribute('required');
            input_for_rent[i].setAttribute('disabled', '');
        }
        // Show error if both checkboxes are unchecked
        if (!sale_check.checked){
            document.getElementById('checkbox-warning').style.display= 'inline';
            document.getElementById('submit-button').setAttribute('disabled',true);
        }
    }
});
function searchISBN(button){
    var isbn = document.getElementById('id_isbn').value;
    if (isbn.length == 13){
        button.href = "?isbn="+document.getElementById('id_isbn').value;
    } else {
        button.href = "{% url 'create-listing' %}";
    }
}
function loadFile() {
    var output = document.getElementById('photo-upload');
    document.getElementById('image_upload').style.display = "none";
    if (event.target.files[0] != undefined){
        output.style.display = "block";
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
            URL.revokeObjectURL(output.src) // free memory
        }
    } else {
        document.getElementById('image_upload').style.display = "flex";
        output.style.display = "none";
    }
}
function deleteImage() {
    document.getElementById('photo-upload').style.display = "none";
    document.getElementById('image_upload').style.display = "flex";
    document.getElementById('image_delete').style.display = "none";
    document.getElementById('id_image').value = null;
}

function addAuthorForm() {
    var authorFormset = document.getElementById('id_author_formset');
    var totalFormCountInput = document.getElementById('id_author-TOTAL_FORMS');
    var totalFormCount = parseInt(totalFormCountInput.value);

    var newForm = authorFormset.rows[authorFormset.rows.length - 1].cloneNode(true);

    newForm.querySelectorAll('input').forEach(function(input) {
        var oldName = input.getAttribute('name');
        input.setAttribute('name', oldName.replace('-' + (totalFormCount - 1) + '-', '-' + totalFormCount + '-'));
        var oldId = input.getAttribute('id');
        input.setAttribute('id', oldId.replace('-' + (totalFormCount - 1) + '-', '-' + totalFormCount + '-'));
        input.value = '';
    });

    authorFormset.appendChild(newForm);

    totalFormCountInput.value = totalFormCount + 1;

    toggleRemoveButtons('id_author_formset', '.author-form', '.remove-author-button');
}

function removeAuthorForm(button) {
    var currentForm = button.parentNode.parentNode;
    var authorLength = document.getElementsByClassName('author-form').length;
    var totalForms = document.getElementById('id_author-TOTAL_FORMS').value;
    if (authorLength > 1){
        currentForm.parentNode.removeChild(currentForm);
        // toggleRemoveButtons('id_author_formset', '.author-form', '.remove-author-button');
        document.getElementById('id_author-TOTAL_FORMS').value = totalForms - 1;
    } else {
        // Clear the fields when remove button is pressed when length is 1
        inputs = document.getElementsByClassName('author-form')[0].getElementsByTagName('input');
        for (var i = 0; i < inputs.length; i ++){
            inputs[i].value = "";
        }
    }
}

function addCourseForm() {
    var courseFormset = document.getElementById('id_course_formset');
    var totalFormCountInput = document.getElementById('id_course-TOTAL_FORMS');
    var totalFormCount = parseInt(totalFormCountInput.value);

    var newForm = courseFormset.lastElementChild.cloneNode(true);

    newForm.querySelectorAll('input').forEach(function(input) {
        var oldName = input.getAttribute('name');
        input.setAttribute('name', oldName.replace('-' + (totalFormCount - 1) + '-', '-' + totalFormCount + '-'));
        var oldId = input.getAttribute('id');
        input.setAttribute('id', oldId.replace('-' + (totalFormCount - 1) + '-', '-' + totalFormCount + '-'));
        input.value = '';
    });

    courseFormset.appendChild(newForm);

    totalFormCountInput.value = totalFormCount + 1;

    toggleRemoveButtons('id_course_formset', '.course-form', '.remove-course-button');
}

function removeCourseForm(button) {
    var currentForm = button.parentNode;
    var courseLength = document.getElementsByClassName('course-form').length;
    var totalForms = document.getElementById('id_course-TOTAL_FORMS').value;
    if (courseLength > 1){
        currentForm.parentNode.removeChild(currentForm);
    // toggleRemoveButtons('id_course_formset', '.course-form', '.remove-course-button');
        document.getElementById('id_course-TOTAL_FORMS').value = totalForms - 1;
    }else{
        inputs = document.getElementsByClassName('course-form')[0].getElementsByTagName('input');
        for (var i = 0; i < inputs.length; i ++){
            inputs[i].value = "";
        }
    }
}

function toggleRemoveButtons(formsetId, formClass, buttonClass) {
    var formset = document.getElementById(formsetId);
    var forms = formset.querySelectorAll(formClass);
    var removeButtons = formset.querySelectorAll(buttonClass);

    // Only show remove button if there are at least two forms
    if (forms.length > 1) {
        removeButtons.forEach(function(button) {
            button.style.display = 'inline-block';
        });
    } else {
        removeButtons.forEach(function(button) {
            button.style.display = 'none';
        });
    }
}
