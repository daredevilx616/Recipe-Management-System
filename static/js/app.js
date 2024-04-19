function searchRecipes() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toUpperCase();
    let recipeList = document.getElementById('recipe-list');
    let recipes = recipeList.getElementsByClassName('recipe-item');

    for (let i = 0; i < recipes.length; i++) {
        let title = recipes[i].getElementsByClassName('recipe-title')[0];
        if (title.innerText.toUpperCase().indexOf(filter) > -1) {
            recipes[i].style.display = "";
        } else {
            recipes[i].style.display = "none";
        }
    }
}
function toggleIngredientsSelection(toggle) {
    const checkboxes = document.querySelectorAll('input[name="ingredients"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = toggle;
    });
}

function toggleRecipeDetails(detailsId) {
    var details = document.getElementById(detailsId);
    var display = details.style.display;
    details.style.display = display === 'block' ? 'none' : 'block';
}

function addIngredient() {
    var nameField = document.getElementById('new_ingredient_name');
    var categorySelect = document.getElementById('new_ingredient_category');
    var name = nameField.value.trim();
    var category = categorySelect.value;
    
    if (name === '') {
        alert('Please enter an ingredient name.');
        return;
    }

    // Create the checkbox for the new ingredient
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = 'ingredients';
    checkbox.value = name; 

    var label = document.createElement('label');
    label.textContent = name + ' (' + category + ')';
    
    label.insertBefore(checkbox, label.firstChild);
    checkbox.checked = true;

    var fieldset = document.querySelector('fieldset');
    fieldset.appendChild(checkbox);
    fieldset.appendChild(label);
    
    // Reset the input fields
    nameField.value = '';
    categorySelect.value = 'Baking'; // Reset to default or first option

    fetch('/add_ingredient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({name: name, category: category}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Ingredient added:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
function deleteIngredient(ingredientId) {
    var ingredientElement = document.getElementById(ingredientId);
    var ingredientValue = ingredientElement.querySelector('input[type="checkbox"]').value;

    fetch('/delete_ingredient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: ingredientValue }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        ingredientElement.remove();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
