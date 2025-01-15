function deleteClient(clientId) {
    fetch("/delete-client", {
      method: "POST",
      body: JSON.stringify({ clientId: clientId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }