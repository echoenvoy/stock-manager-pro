

// Theme Toggle with persistence
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = themeToggle.querySelector('i');

// Check for saved user preference, if any, on page load
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    themeIcon.classList.remove('fa-moon');
    themeIcon.classList.add('fa-sun');
} else if (savedTheme === 'light') {
    document.body.classList.remove('dark-mode');
    themeIcon.classList.remove('fa-sun');
    themeIcon.classList.add('fa-moon');
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
    }
});
    
//Make date in readable date
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
  }

//Notification
function showNotification(message, type) {
      const notif = document.getElementById("notification");
      notif.textContent = message;
      notif.className = `notification ${type}`;
      notif.style.display = 'block';
      setTimeout(() => notif.style.display = 'none', 3000);
}



 //Retrieves the list of products from localStorage as a JSON array.
function getStock() {
    return JSON.parse(localStorage.getItem("stock")) || [];
}// Saves the given product list to localStorage
function saveStock(stock) {
    localStorage.setItem("stock", JSON.stringify(stock));
}
  //Export the current product list to an Excel file using SheetJS.
function exportStock() {
    const stock = getStock(); // assumes you already have getStock()

    if (stock.length === 0) {
      alert("No products to export.");
      return;
    }

    const worksheet = XLSX.utils.json_to_sheet(stock); // convert JSON to sheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Stock");

    XLSX.writeFile(workbook, "stock-data.xlsx"); // download file
}


//Delivery :
    //Retrieves the list of deliveries from localStorage.

function getDelivery() {
      const data = localStorage.getItem("delivery");
      if (!data || data === "undefined") return [];
      try {
        return JSON.parse(data);
      } catch (e) {
        console.error("Erreur lors du parsing JSON de delivery :", e);
        return [];
      }
    }
    //Saves the deliveries list to localStorage.
function saveDelivery(data) {
    localStorage.setItem("delivery", JSON.stringify(data));
 }

//Export  the delivery list to an Excel file with a timestamp.
function exportDelivery() {
    const delivery = getDelivery(); // assumes you already have getDelivery()

    if (delivery.length === 0) {
      alert("No Delivery to export.");
      return;
    }

      // Get current date and time
    const now = new Date();
    const exportTime = now.toLocaleString(); // e.g., "27/07/2025, 11:22:33"

    // Insert export time as the first row (with a label)
    const headerRow = [{ "Exported At": exportTime }];
    const dataWithHeader = headerRow.concat(delivery);

    // Convert to worksheet
    const worksheet = XLSX.utils.json_to_sheet(dataWithHeader, { skipHeader: false });

    // Create workbook and append worksheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "delivery");

    // Save the file
    XLSX.writeFile(workbook, "delivery-data.xlsx");
}



//Employee
//Retrieves the list of employees from localStorage as a JSON array.
function getEmployee() {
    return JSON.parse(localStorage.getItem("employee")) || [];
}

// Saves the given employee list to localStorage
function saveEmployee(employee) {
    localStorage.setItem("employee", JSON.stringify(employee));
}
 
