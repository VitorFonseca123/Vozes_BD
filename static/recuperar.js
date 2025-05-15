function confirmarExclusao(botao) {
    //console.log(botao);
    const confirmado = confirm("Tem certeza que deseja excluir?");
    console.log(botao.closest('tr').cells[5].innerText);
    if (confirmado == true) {
     
      const linha = botao.closest('tr');
      const audioPath = linha.cells[5].innerText;
      
      //mandar pro python
      fetch('/excluir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                audio_path: audioPath
            })
        })
        .then(response => response.json())
        .then(data => {
            alert("Exclusão realizada com sucesso!");
            linha.remove(); 
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao excluir.");
        });
      
    } else {
      // Cancelado
      console.log("Exclusão cancelada.");
    }
  }