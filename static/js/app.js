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

function toggleRecipeDetails(recipeId) {
    const detailsElement = document.getElementById(recipeId);
    if (detailsElement.style.display === 'none') {
        detailsElement.style.display = 'block';
    } else {
        detailsElement.style.display = 'none';
    }
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

function editRecipe(recipeId) {
    // Get the existing data
    var title = document.querySelector(`#title-${recipeId}`).innerText;
    var instructions = document.querySelector(`#details-${recipeId} p:first-child`).innerText;
    var ingredients = document.querySelector(`#details-${recipeId} p:last-child span`).innerText;

    // Convert recipe details to editable fields
    document.getElementById(`details-${recipeId}`).innerHTML = `
        <label>Title:</label>
        <input type="text" id="edit-title-${recipeId}" value="${title}" onclick="event.stopPropagation();">
        <label>Instructions:</label>
        <textarea id="edit-instructions-${recipeId}" onclick="event.stopPropagation();">${instructions}</textarea>
        <label>Ingredients:</label>
        <textarea id="edit-ingredients-${recipeId}" onclick="event.stopPropagation();">${ingredients}</textarea>
        <button onclick="saveRecipe(${recipeId})">Save</button>
        <button onclick="cancelEdit(${recipeId})">Cancel</button>
    `;
}


function saveRecipe(recipeId) {
    // Get the updated data
    var updatedTitle = document.getElementById('edit-title-' + recipeId).value;
    var updatedInstructions = document.getElementById('edit-instructions-' + recipeId).value;
    var updatedIngredients = document.getElementById('edit-ingredients-' + recipeId).value;

    // Construct the payload
    var payload = {
        title: updatedTitle,
        instructions: updatedInstructions,
        ingredients: updatedIngredients.split(',').map(ingredient => ingredient.trim()) // Assuming you want an array of ingredients
    };

    // Send the update to the server
    fetch('/update_recipe/' + recipeId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI to show the saved changes or handle errors
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function cancelEdit(recipeId) {
    // Reload the page or re-fetch the recipe details to cancel the edit
    window.location.reload();
}

// function loadIngredients(recipeId) {
//     fetch(`/get_ingredients/${recipeId}`)
//     .then(response => response.json())
//     .then(ingredients => {
//         const ingredientsFieldset = document.getElementById('ingredients-fieldset');
//         ingredientsFieldset.innerHTML = ''; // Clear existing options
//         ingredients.forEach(ingredient => {
//             const ingredientDiv = document.createElement('div');
//             ingredientDiv.className = 'ingredient-item';
//             ingredientDiv.id = `ingredient-${ingredient.ingredient_id}`;

//             const checkbox = document.createElement('input');
//             checkbox.type = 'checkbox';
//             checkbox.name = 'ingredients';
//             checkbox.value = ingredient.ingredient_id;
//             checkbox.checked = ingredient.included; // Set based on if it's included in the recipe

//             const label = document.createElement('label');
//             label.textContent = ingredient.name;

//             const deleteSpan = document.createElement('span');
//             deleteSpan.className = 'delete-icon';
//             deleteSpan.textContent = '×';
//             deleteSpan.onclick = () => deleteIngredient(`ingredient-${ingredient.ingredient_id}`);

//             ingredientDiv.appendChild(checkbox);
//             ingredientDiv.appendChild(label);
//             ingredientDiv.appendChild(deleteSpan);

//             ingredientsFieldset.appendChild(ingredientDiv);
//         });
//     })
//     .catch(error => console.error('Error loading ingredients:', error));
// }
