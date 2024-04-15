function searchRecipes() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toUpperCase();
    let ul = document.getElementById('recipeList');
    let li = ul.getElementsByTagName('li');

    for (let i = 0; i < li.length; i++) {
        let txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
