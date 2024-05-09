        function filterFiles() {
            // Obtener el texto del campo de búsqueda y convertir a minúsculas para una comparación sin distinción de mayúsculas
            const searchValue = document.getElementById('search-input').value.toLowerCase();

            // Obtener todos los elementos div con clase "file"
            const fileDivs = document.querySelectorAll('.file');

            // Iterar sobre cada div para determinar si debe mostrarse o ocultarse
            fileDivs.forEach(div => {
                // Obtener el contenido del párrafo dentro del enlace y convertir a minúsculas para comparación
                const paragraphText = div.querySelector('a p').textContent.toLowerCase();

                // Mostrar u ocultar según la coincidencia del texto
                if (paragraphText.includes(searchValue)) {
                    div.classList.remove('hidden'); // Mostrar si coincide
                } else {
                    div.classList.add('hidden'); // Ocultar si no coincide
                }
            });
        }
