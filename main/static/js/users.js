$(document).ready(function () {
    let $tablaUsuarios = $("#tablaUsuarios");
    let table;

    if ($tablaUsuarios.length) {
        // Destruir DataTable solo si ya está inicializado
        if ($.fn.DataTable.isDataTable($tablaUsuarios)) {
            $tablaUsuarios.DataTable().clear().destroy();
        }

        // Inicializar DataTable
        table = $tablaUsuarios.DataTable({
            paging: true,
            autoWidth: true,
            responsive: true,
            language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "No se encontraron registros",
                info: "Mostrando página _PAGE_ de _PAGES_",
                infoEmpty: "No hay registros disponibles",
                infoFiltered: "(filtrado de _MAX_ registros en total)",
                search: "Buscar:",
                paginate: {
                    next: "Siguiente",
                    previous: "Anterior"
                }
            },
            lengthMenu: [5, 10, 25, 50],
            order: [[1, "asc"]] // Ordenar filas por nombre
        });
    }

    // Delegación de eventos para botones dinámicos
    $(document).on("click", ".actualizar-btn", function () {
        let userId = $(this).data("id");
        let username = $(this).data("username");
        let email = $(this).data("email");

        $("#editUserId").val(userId);
        $("#editUsername").val(username);
        $("#editEmail").val(email);
        $("#editPassword").val(""); // Vacío por defecto

        $("#modalEditarUsuario").modal("show");
    });

    // Manejar la actualización de usuario
    $("#formEditarUsuario").submit(function (event) {
        event.preventDefault();
        
        let userId = $("#editUserId").val();
        let updatedData = {
            username: $("#editUsername").val(),
            email: $("#editEmail").val(),
            password: $("#editPassword").val() || null // Enviar null si no hay cambio de contraseña
        };

        $.ajax({
            url: `/usuarios/editar/${userId}`, 
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(updatedData),
            success: function () {
                alert("Usuario actualizado correctamente");
                location.reload();
            },
            error: function () {
                alert("Error al actualizar usuario");
            }
        });        
    });

    // Manejo de eliminación de usuario
    $(document).on("click", ".eliminar-btn", function () {
        let userId = $(this).data("id");

        if (confirm("¿Seguro que quieres eliminar este usuario?")) {
            $.ajax({
                url: `/usuarios/eliminar/${userId}`, 
                type: "POST",
                success: function (response) {
                    alert(response.message); // Muestra el mensaje de éxito desde el servidor
                    location.reload(); // Recarga la página
                },
                error: function (xhr) {
                    let errorMessage = xhr.responseJSON ? xhr.responseJSON.error : "Error al eliminar usuario.";
                    alert(errorMessage); // Muestra el mensaje de error real
                }
            });
        }
    });
});