const expenseURL = '/Chart'
const incomeURL = '/income/Chart'

let income = document.querySelector("#income")
let expense = document.querySelector("#expense")
let income_summary = document.querySelector("#income-summary")
let expense_summary = document.querySelector("#expense-summary")

const color_set = ['rgba(255, 99, 132, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(255, 206, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 159, 64, 0.5)',
    'rgb(63, 63, 191, 0.5)',
    'rgb(224, 15, 196, 0.5)',
    'rgb(245, 224, 34, 0.5)',
    'rgb(3, 231, 41, 0.5)',
    'rgba(235,4,119, 0.5)',
    'rgba(18,39,190, 0.5)',
    'rgba(252,70,107, 0.5)',
    'rgba(63,94,251 ,0.5)']

if (expense) {
    fetch(expenseURL).then(res => res.json()).then(data => {

        let labels = []

        data.forEach(item => {
            if (labels.includes(item.category) === false) {
                labels.push(item.category)
            }
        })

        let expense_data = [];

        for (let i = 0; i < labels.length; i++) {
            expense_data.push(0)
        }

        for (let i = 0; i < labels.length; i++) {
            data.forEach(item => {
                if (labels[i] === item.category) {
                    expense_data[i] = expense_data[i] + item.amount
                }
            })
        }

        console.log(expense_data)

        let background_colors = []

        for (let i = 0; i < labels.length; i++) {
            let chosen_color = color_set[Math.floor(Math.random() * color_set.length)]
            while (background_colors.includes(chosen_color)) {
                chosen_color = color_set[Math.floor(Math.random() * color_set.length)]
            }
            background_colors.push(chosen_color)
        }


        let ctx = document.querySelector("#myChart").getContext("2d");
        let myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'expense',
                    data: expense_data,
                    backgroundColor: background_colors,
                    borderColor: background_colors,
                    borderWidth: 1
                }]
            },
            options: {
                legend: {
                    labels: {
                        FontSize: 50
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                }
            }
        });
    });
}

if (income) {
    fetch(incomeURL).then(res => res.json()).then(data => {

        let labels = []
        console.log(data)
        data.forEach(item => {
            if (labels.includes(item.source) === false) {
                labels.push(item.source)
            }
        })

        let income_data = [];

        for (let i = 0; i < labels.length; i++) {
            income_data.push(0)
        }

        for (let i = 0; i < labels.length; i++) {
            data.forEach(item => {
                if (labels[i] === item.source) {
                    income_data[i] = income_data[i] + item.amount
                }
            })
        }

        console.log(income_data)

        let background_colors = []

        for (let i = 0; i < labels.length; i++) {
            let chosen_color = color_set[Math.floor(Math.random() * color_set.length)]
            while (background_colors.includes(chosen_color)) {
                chosen_color = color_set[Math.floor(Math.random() * color_set.length)]
            }
            background_colors.push(chosen_color)
        }


        let ctx = document.querySelector("#myChart").getContext("2d");
        let myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'income',
                    data: income_data,
                    backgroundColor: background_colors,
                    borderColor: background_colors,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });
}

if (expense_summary) {

}