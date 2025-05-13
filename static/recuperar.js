function confirmarExclusao() {
    const confirmado = confirm("Tem certeza que deseja excluir?");
    if (confirmado) {
      // Coloque aqui a ação de exclusão
      alert("Item excluído com sucesso!"); 
    } else {
      // Cancelado
      console.log("Exclusão cancelada.");
    }
  }