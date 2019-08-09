document.addEventListener('DOMContentLoaded', function () {
  // when user clicks create task button
  document.querySelector('#taskButton').onclick = (e) => {
    let base_url = `${location.protocol}//${document.domain}:${location.port}`;
    let endpoint = base_url + "/dashboard/createtask";
    // AJAX request to load the content from createtask route
    const request = new XMLHttpRequest();
    request.open('GET', endpoint);
    request.send();

    request.onload = () => {
      const response = request.responseText;
      document.querySelector('#basicModal').innerHTML = response;
    };
  }
});
