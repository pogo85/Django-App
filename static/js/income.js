const delete_set = document.querySelectorAll('.delete-item');
const searchField = document.querySelector('#searchField')
const table_output = document.querySelector('.table_output')
const app_table = document.querySelector('.app_table')
const pagination = document.querySelector('.pagination-container')
const tbody = document.querySelector('.table-output-body')
const no_results = document.querySelector('.no-results')

table_output.style.display = 'none'
app_table.style.display = 'block'
pagination.style.display = 'block'
no_results.style.display = 'none'

const edit_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>'
const delete_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="red" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>'


for (let i = 0; i < delete_set.length; i++) {
    delete_set[i].addEventListener('click', (e) => {
        alert('Are you sure you want to delete')
    })
}

searchField.addEventListener('keyup', (e) => {
    const search_value = e.target.value
    if (search_value.trim().length > 0) {
        tbody.innerHTML = ''
        console.log('search_value', search_value)
        fetch('/income/search_income', {
            body: JSON.stringify({'search_value': search_value}),
            method: 'POST'
        }).then(
            res => res.json()
        ).then(
            data => {
                console.log(data)
                app_table.style.display = 'none'
                table_output.style.display = 'block'
                pagination.style.display = 'none'
                if (data.length === 0) {
                    table_output.style.display = 'none'
                    no_results.style.display = 'block'
                } else {
                    no_results.style.display = 'none'

                    data.forEach(item => {
                        tbody.innerHTML += `
                            <tr>
                                <td>${item.amount}</td>
                                <td>${item.source}</td>
                                <td>${item.description}</td>
                                <td>${item.date}</td>
                                <td><a href="/income/edit_income/${item.id}" class="">${edit_svg}</a></td>
                                <td><a href="/income/delete_income/${item.id}" class="delete-item">${delete_svg}</a>
                                </td>      
                                      
                            </tr>
                        `
                    })
                }
            }
        )
    } else {
        table_output.style.display = 'none'
        app_table.style.display = 'block'
        pagination.style.display = 'block'
        no_results.style.display = 'none'
    }
})