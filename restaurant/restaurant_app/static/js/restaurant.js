function writeOrderList() {
    var request = new XMLHttpRequest();
    var url = "/api/orders";
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var order_table_div = document.getElementById("order_table_div");
            order_table_div.innerHTML = "";
            var table = document.createElement("table");
            var th_row = document.createElement("tr");
            var th1 = document.createElement("th");
            th1.textContent = "Order ID";
            var th2 = document.createElement("th");
            th2.textContent = "Order Date";
            th_row.appendChild(th1);
            th_row.appendChild(th2);
            table.appendChild(th_row);
            data.forEach(function(order) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                var a = document.createElement("a");
                a.setAttribute("href", "/order/" + order.order_id);
                a.textContent = order.order_id;
                td1.appendChild(a);
                var td2 = document.createElement("td");
                td2.textContent = order.order_date;
                tr.appendChild(td1);
                tr.appendChild(td2);
                table.appendChild(tr);
            });
            order_table_div.appendChild(table);
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("write order list request failed: " + this.status);
        }
    }
    request.open("GET", url, true);
    request.send();
}

function writeOrderDetail(order_id) {
    var request = new XMLHttpRequest();
    var url = "/api/order/" + order_id;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var order_info_div = document.getElementById("order_info_div");
            order_info_div.innerHTML = "";
            var p1 = document.createElement("p");
            p1.textContent = "Order ID: " + data.order_id;
            var p2 = document.createElement("p");
            p2.textContent = "Order Date: " + data.order_date;
            order_info_div.appendChild(p1);
            order_info_div.appendChild(p2);

            var product_info_div = document.getElementById("product_info_div");
            product_info_div.innerHTML = "";
            var table = document.createElement("table");
            var th_row = document.createElement("tr");
            var th1 = document.createElement("th");
            th1.textContent = "Product Name";
            var th2 = document.createElement("th");
            th2.textContent = "Price";
            var th3 = document.createElement("th");
            th3.textContent = "Quantity";
            var th4 = document.createElement("th");
            th4.textContent = "Subtotal";
            th_row.appendChild(th1);
            th_row.appendChild(th2);
            th_row.appendChild(th3);
            th_row.appendChild(th4);
            table.appendChild(th_row);
            var total_price = 0;
            data.product_data.forEach(function(product) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                td1.textContent = product.product_name;
                var td2 = document.createElement("td");
                td2.textContent = product.price.toFixed(2);
                var td3 = document.createElement("td");
                td3.textContent = product.quantity;
                var td4 = document.createElement("td");
                td4.textContent = (product.price * product.quantity).toFixed(2);
                total_price += product.price * product.quantity;
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                tr.appendChild(td4);
                table.appendChild(tr);
            });
            product_info_div.appendChild(table);

            var total_price_p = document.getElementById("total_price");
            total_price_p.textContent = "Total Price: " + total_price.toFixed(2);
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("write order detail request failed: " + this.status);
        }
    }
    request.open("GET", url, true);
    request.send();
}

function addRow() {
    var table = document.getElementById("product_table");
    var new_row = table.insertRow(table.rows.length);
    var cell1 = new_row.insertCell(0);
    var cell2 = new_row.insertCell(1);
    var cell3 = new_row.insertCell(2);
    cell1.innerHTML = '<input type="text" name="product_name" required>';
    cell2.innerHTML = '<input type="number" min="1" max="100" name="quantity" required>';
    cell3.innerHTML = '<a href="javascript:void(0)" onClick="deleteRow(this)">Delete</a>';
}

function deleteRow(row) {
    var row_index = row.parentNode.parentNode.rowIndex;
    document.getElementById("product_table").deleteRow(row_index);
}

function createOrder(event) {
    event.preventDefault();
    var form = document.getElementById("create_order_form");
    var form_data = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/order/new";
    var alert_shown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Order created successfully!");
            window.location.href = "/order/" + form_data.get(form_data.keys().next().value);
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("create order request failed: " + this.status);
            if (this.status == 400 && JSON.parse(this.responseText).error == "UNIQUE constraint failed: restaurant_app_order.order_id" && !alert_shown) {
                alert("Order ID already exists. Please choose a different Order ID.");
                alert_shown = true;
            }
            if (this.status == 400 && JSON.parse(this.responseText).error.includes("It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.") && !alert_shown) {
                alert("Order date must be in YYYY-MM-DD HH:MM:SS.");
                alert_shown = true;
            }
        }
    }
    request.open("POST", url, true);
    request.send(form_data);
}

function writeUpdateForm(order_id) {
    var request = new XMLHttpRequest();
    var url = "/api/order/" + order_id;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var order_id_input = document.getElementById("order_id");
            order_id_input.value = data.order_id;
            order_id_input.disabled = true;
            var hidden_order_id_input = document.getElementById("hidden_order_id");
            hidden_order_id_input.value = data.order_id;
            var order_date_input = document.getElementById("order_date");
            order_date_input.value = data.order_date;
            var table = document.getElementById("product_table");
            data.product_data.forEach(function(product) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                var input1 = document.createElement("input");
                input1.type = "text";
                input1.name = "product_name";
                input1.required = true;
                input1.value = product.product_name;
                var td2 = document.createElement("td");
                var input2 = document.createElement("input");
                input2.type = "number";
                input2.min = 1;
                input2.max = 100;
                input2.name = "quantity";
                input2.required = true;
                input2.value = product.quantity;
                var td3 = document.createElement("td");
                var a = document.createElement("a");
                a.href = "javascript:void(0)";
                a.textContent = "Delete";
                a.onclick = function() {
                    deleteRow(this);
                };
                td1.appendChild(input1);
                td2.appendChild(input2);
                td3.appendChild(a);
                tr.appendChild(td1);
                tr.appendChild(td2);
                tr.appendChild(td3);
                table.appendChild(tr);
            });
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("write update form request failed: " + this.status);
        }
    }
    request.open("GET", url, true);
    request.send();
}

function updateOrder(event, order_id) {
    event.preventDefault();
    var form = document.getElementById("update_order_form");
    var form_data = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/order/" + order_id;
    var alert_shown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Order updated successfully!");
            window.location.href = "/order/" + order_id;
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("update order request failed: " + this.status);
            if (this.status == 400 && JSON.parse(this.responseText).error.includes("It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.") && !alert_shown) {
                alert("Order date must be in YYYY-MM-DD HH:MM:SS.");
                alert_shown = true;
            }
        }
    }
    request.open("PUT", url, true);
    request.send(form_data);
}

function deleteOrder(order_id) {
    var confirm_delete = confirm("Are you sure you want to delete this order?");
    if (confirm_delete) {
        var request = new XMLHttpRequest();
        var url = "/api/order/" + order_id;
        request.onreadystatechange = function() {
            if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
                alert("Order deleted successfully!");
                window.location.href = "/orders";
            }
            else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
                console.log("delete order request failed: " + this.status);
            }
        }
        request.open("DELETE", url, true);
        request.send();
    }
}

function writeProductList() {
    var request = new XMLHttpRequest();
    var url = "/api/products";
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            var data = JSON.parse(this.responseText);
            var product_table_div = document.getElementById("product_table_div");
            product_table_div.innerHTML = "";
            var table = document.createElement("table");
            var th_row = document.createElement("tr");
            var th1 = document.createElement("th");
            th1.textContent = "Product Name";
            var th2 = document.createElement("th");
            th2.textContent = "Price";
            th_row.appendChild(th1);
            th_row.appendChild(th2);
            table.appendChild(th_row);
            data.forEach(function(product) {
                var tr = document.createElement("tr");
                var td1 = document.createElement("td");
                td1.textContent = product.product_name;
                var td2 = document.createElement("td");
                td2.textContent = product.price;
                tr.appendChild(td1);
                tr.appendChild(td2);
                table.appendChild(tr);
            });
            product_table_div.appendChild(table);
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("write product list request failed: " + this.status);
        }
    }
    request.open("GET", url, true);
    request.send();
}

function createProduct(event) {
    event.preventDefault();
    var form = document.getElementById("create_product_form");
    var form_data = new FormData(form);
    var request = new XMLHttpRequest();
    var url = "/api/product/new";
    var alert_shown = false;
    request.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status >= 200 && this.status < 400)) {
            alert("Product created successfully!");
            window.location.href = "/products";
        }
        else if (this.status >= 400 || (this.status > 0 && this.status < 200)) {
            console.log("create product request failed: " + this.status);
            if (this.status == 400 && JSON.parse(this.responseText).error == "UNIQUE constraint failed: restaurant_app_product.product_name" && !alert_shown) {
                alert("Product name already exists. Please choose a different product name.");
                alert_shown = true;
            }
        }
    }
    request.open("POST", url, true);
    request.send(form_data);
}