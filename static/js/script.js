
const navLinks = document.querySelectorAll('nav ul li a') // Select all navigation links inside the 'nav ul li a' elements
const dropdown = document.getElementById('dropdown-description') // Get the dropdown element where descriptions will be displayed

// Loop through each navigation link and add event listeners
navLinks.forEach(link => {
    link.addEventListener('mouseover', (event)=> {
         // Get the description stored in the 'data-description' attribute of the hovered link
        const description = event.target.getAttribute('data-description');
        // Get the position of the hovered link relative to the viewport
        const rect = event.target.getBoundingClientRect();

         // Update the dropdown content with the description text
        dropdown.textContent = description;
        // Make the dropdown visible
        dropdown.style.display = 'block';
        dropdown.style.opacity = '1';
        dropdown.style.visibility = 'visible';

        // Calculate the dropdown position below the link (adjusted by -75 pixels for styling)
        let dropdownTop = rect.bottom + window.scrollY - 75
        let dropdownLeft = rect.left

        // Get the width and height of the dropdown
        const dropdownWidth = dropdown.offsetWidth;
        const dropdownHeight = dropdown.offsetHeight;

        // Get the width and height of the viewport
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;

        // Ensure the dropdown does not overflow beyond the screen width
        if(dropdownLeft + dropdownWidth > screenWidth) {
            dropdownLeft = screenWidth - dropdownWidth - 10 // Adjust to fit within screen
        }
         // Ensure the dropdown does not overflow beyond the screen height
        if(dropdownTop + dropdownHeight > screenHeight){
            dropdownTop = rect.top + window.scrollY - 75 // Adjust position to fit within screen
        }

         // Apply the calculated position to the dropdown
        dropdown.style.top = `${dropdownTop}px`
        dropdown.style.left = `${dropdownLeft}px`
    })

    // Hide the dropdown when the mouse leaves the link
    link.addEventListener('mouseout', ()=>{
        dropdown.style.opacity = '1'
        dropdown.style.visibility = 'hidden'
    })
})   

// jQuery function to handle file upload when the document is ready
$(document).ready(function(){
    // When the form is submitted
    $("#upload-form").submit(function (event) {
        event.preventDefault(); // Prevent default form submission behavior

        var formData = new FormData(); // Create a FormData object for file upload
        var fileInput = $("#file-input")[0].files[0]; // Get the selected file
        formData.append("file", fileInput); // Append the file to FormData

        // Send an AJAX request to the "/upload" route
        $.ajax({
            url: "/upload", // Backend API endpoint for file upload
            type: "POST", // HTTP method
            data: formData, // Data to send
            processData: false, // Prevent automatic processing of data
            contentType: false, // Prevent automatic content type setting
            success: function (response) {
                if(response) {
                    var summary = response; // Store the received response

                     // Construct HTML to display the file analysis summary
                    var summaryHTML = `
                        <p><strong>File Type:</strong> {${summary['File Type']}}</p>
                        <p><strong>Size:</strong> {${summary['Size (bytes)']} bytes}</p>
                        <p><strong>Extracted Summary:</strong></p>
                        <ul>
                            <li><strong>Attack Type:</strong> {${summary['Extracted Summary']['Attack Type']}}</li>
                            <li><strong>Date:</strong> {${summary['Extracted Summary']['Date'] }}</li>
                            <li><strong>Affected Systems:</strong> {${summary['Extracted Summary']['Affected Systems'] }}</li>
                        </ul>
                    `;
                     // Insert the generated summary HTML into the #summary-content div
                    $("#summary-content").html(summaryHTML)
                } 
            },
            error: function (xhr, status, error) {
                alert("Error: " + xhr.responseText); // Show an alert if an error occurs
            }
        });
    });
});