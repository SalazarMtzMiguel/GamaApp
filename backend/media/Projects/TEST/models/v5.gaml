model competencia

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

global
{
	// primero establecemos las dimensiones del mundo y declaramos la variable para identificar las celdas basura
	int largo_mundo <- 10;
	int ancho_mundo <- 10;
	int num_carros <- 1;
	int basura_en_mundo <- 25;
	bool bote_lleno <- false;
	mundo celda_basura; // esta variable de tipo "mundo" es en realidad una variable de tipo "celda" ya que "mundo" es un grid 
										 // y por lo tanto es un conjunto de celdas.
	 
	// Este es el constructor de los agentes que recogen basura/tapan hoyos, se les da una ubicación inicial y nombre
	init
	{
		loop i from: 1 to: 1
		{
			create carro number: 1 // creamos un carro por cada ciclo
			{
			// Establecemos como la celda actual del agente a una de las celdas del grid (llamado mundo) cuyo atributo
			// esta_desocupada sea verdadero, y luego hacemos que dicha celda se marque como no ocupada.
			celda_actual <- one_of(mundo where (each.esta_desocupada));
			celda_actual.esta_desocupada <- false;
			location <- celda_actual.location; // aqui establecemos la ubicación del agente
			name <- "[Carroza_" + i + " de Diego] "; // aquí le damos un nombre
			
			status_mental <- "perdido"; // el agente está originalmente perdido
			status_mov <- "libre"; // el agente originalmente se puede mover libremente
			direccion <- "arriba"; // el agente inicia queriendo moverse hacia arriba para buscar el origen del mundo.
			cargando_basura <- false; // indica que el agente no está cargando basura
			}
			create rickmovil number: 1 // creamos un carro por cada ciclo
			{
			// Establecemos como la celda actual del agente a una de las celdas del grid (llamado mundo) cuyo atributo
			// esta_desocupada sea verdadero, y luego hacemos que dicha celda se marque como no ocupada.
			celda_actual <- one_of(mundo where (each.esta_desocupada));
			celda_actual.esta_desocupada <- false;
			location <- celda_actual.location; // aqui establecemos la ubicación del agente
			name <- "[Carroza_" + i + " de Rick]  "; // aquí le damos un nombre
			status_mental <- "perdido"; // el agente está originalmente perdido
			status_mov <- "libre"; // el agente originalmente se puede mover libremente
			direccion <- "arriba"; // el agente inicia queriendo moverse hacia arriba para buscar el origen del mundo.
			cargando_basura <- false; // indica que el agente no está cargando basura
			}
		}
	// aquí generamos las celdas que tienen basura, marcándolas con el color adecuado y cambiando su atributo correspondiente
		loop times: basura_en_mundo
		{
			// se selecciona una celda del mundo que esté desocupada y que no tenga basura y se indica que está sucia por medio del color verde
			celda_basura <- one_of(mundo where (each.esta_desocupada and each.color=#white));
			celda_basura.color <- #green;
			celda_basura.esta_sucia <- true;
		}
		// aquí creamos el bote de basura y lo ubicamos en algún lugar desocupado del mundo que no esté sucio ni ocupado
		create bote number: 1
		{
			// primero ubicamos al bote en una celda que no esté ocupada ni sucia
			celda_ubicacion <- one_of(mundo where(each.esta_desocupada and each.color=#white));
			celda_ubicacion.tiene_bote <- true; // se le dice a la celda en cuestión que el bote está sobre ella
			location <- celda_ubicacion.location; // aqui establecemos la ubicación del agente
			capacidad <- basura_en_mundo; // capacidad máxima del bote (igual a la cantidad de basura en el mundo)
			cantidad_de_basura <- 0; // cantidad de basura actual en el bote
		}	
	}
	// aquí se establece la condición de término de la simulación, que es cuando el bote se llena
	reflex termina_simulacion when: bote_lleno = true
	{
		do pause; // pausa la simulación
	}
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Creamos el agente grid (que llamamos mundo) donde viven los agentes, y establecemos la convención de vecinos que se va a usar.
// Cabe destacar que el agente mundo de tipo grid es en realidad un conjunto de agentes celda, y los atributos que se le den a grid, en realidad son
// los atributos de cada una de las celdas
grid mundo width: largo_mundo height: ancho_mundo neighbors: 4
{
	bool esta_desocupada <- true; // este atributo aplica a cada celda e indica si está desocupada, se inicializa en verdadero
	bool esta_sucia <- false; // este atributo aplica a cada celda e indica si la celda tiene basura, se inicializa en falso.
	bool tiene_bote <- false; // Nos indica si hay un bote en esa celda.
}

// Creamos la especie carro, a la cual se le da la habilidad de moverse
species rickmovil skills: [moving]
{	
	// los primeros dos atributos son del tipo "mundo" por lo que son en realidad del tipo "celda" y por lo tanto heredan los atributos de dicha clase.
	mundo celda_actual; // celda actual del agente (carro)
	mundo celda_siguiente; // celda objetivo, a donde se va a mover el agente
	mundo celda_anterior; // celda que el agente visitó en el paso anterior
	mundo ultima_celda_exp; //ultima celda que tocó en modo exploración
	string ultima_direccion_exp; // ultima dirección que tuvo al estar en modo exploración
	
	string name; // nombre del agente
	string direccion;
	string status_mental; // estado mental del agente, determina sus acciones
	string status_mov; // estado de movimiento del agente, indica si el movimiento solicitado fue posible o no
	string last_mov; 
	bool cargando_basura;
	bool one_step <- true;
	bool verbose <- true;
	int basura_entregada <- 0;
	int x <- 0;
	int y <- 0;
	list<mundo> ubicacion_basura <- []; // lista de ubicaciones de la basura en el mundo
	list<mundo> ubicacion_basura_coords <- []; 
	mundo ubicacion_bote; // ubicacion del bote una vez que lo encuentre
	
	reflex end_game when: bote_lleno = true{
		if verbose{
			write name + "Numero final de basura recolectada: " + basura_entregada;
		}
	}
	
	// Mapea la basura, y el bote en el mundo
	reflex actualizar_percepcion{
		if celda_actual.color = #green and not(celda_actual in ubicacion_basura) // si el color de la celda actual es verde (está sucia) y no está ya en la lista de ubicaciones:
		{ 
			add celda_actual to: ubicacion_basura;
			if verbose{
			write name + "¡Basura encontrada" + ubicacion_basura;
			}
			ubicacion_basura <- ubicacion_basura sort_by (each);
			if not(ubicacion_bote = nil){
				ubicacion_basura <- ubicacion_basura sort_by (each.grid_x);
			}
			//write "y: " + (celda_actual.grid_x) mod ancho_mundo;
			//write "x: " + (celda_actual.grid_y) mod largo_mundo;
		}
		if (ubicacion_bote = nil) and celda_actual.tiene_bote and status_mental = "explorando" // si la celda actual tiene el bote y aún no se conoce la ubicación del bote:
		{
			ubicacion_bote <- celda_actual;
			if verbose{
			write name + "¡Bote encontrado! En celda "+ celda_actual;				
			}
			ubicacion_basura <- ubicacion_basura sort_by (abs(abs(each.grid_x - ubicacion_bote.grid_x)) + abs((each.grid_y - ubicacion_bote.grid_y)));
		}
	}
	
	// Se dirige hacia (n,n)
	reflex busca_n_n when: status_mental = "perdido"{ // Cambiar a ubicado
		// El agente empieza viendo hacia arriba
		if status_mov = "libre" and direccion = "arriba"{
			direccion <- "abajo";
			last_mov <- "arriba";
			if verbose{
				write name + "Hacia abajo";
			}
		}
		if status_mov = "libre" and direccion = "abajo" and last_mov = "arriba"{
			status_mov <- avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "abajo" and last_mov = "arriba"{
			direccion <- "derecha";
			status_mov <- "libre";
			last_mov <- "abajo";
			if verbose{
				write name + "Hacia derecha";
			}
		}
		if status_mov = "libre" and direccion = "derecha" and last_mov = "abajo"{
			status_mov <- avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "derecha" and last_mov = "abajo"{
			status_mov <- "libre";
			direccion <- "arriba";
			status_mental <- "ubicado";
			if verbose{
				write name + "Hacia arriba";
			}
		}
		if verbose{
			write name + "busca_n_n" + " " + status_mov + " " + status_mental + " " + direccion + " " + ubicacion_basura;
		}		
	}
	
	// Antes: abajo derecha hacia (n,n)
	// Ahora: hacia origen (0,0)
	reflex mide_mundo when: status_mental = "ubicado"{
		if status_mov = "libre" and direccion = "arriba"{
			status_mov <- avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "arriba"{
			direccion <- "izquierda";
			status_mov <- "libre";
			if verbose{
				write name + "Hacia izquierda";
			}	
		}
		if status_mov = "libre" and direccion = "izquierda"{
			status_mov <-  avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "izquierda"{
			status_mental <- "explorando";
			status_mov <- "libre";
			direccion <- "abajo";
			if verbose{
				write name + "Hacia abajo";
			}	
		}
		if verbose{
			write name + "mide_mundo" + " " + status_mov + " " + status_mental + " " + direccion + " " + ubicacion_basura;
		}	
	}
	
	reflex recordar when: status_mental = "explorando" and not(ubicacion_basura = []) and not(ubicacion_bote = nil){
		// Primero guarda la celda actual (que será la del bote) y dirección de movimiento para poder reanudar la exploración una vez que haya entregado la basura. 
		ultima_celda_exp <- celda_actual; //guarda la celda actual como ultima celda explorada
		ultima_direccion_exp <- direccion; // guarda su dirección de movimiento actual como la ultima dirección antes de salir del estado "explorando"
		status_mental <- "recordando";
	}
	
	//explora hasta encontrar el bote de basura
	reflex explorar_mundo when: status_mental = "explorando"{
		if (direccion = "abajo" and celda_actual.grid_y = 0 and celda_actual.grid_x = 0 and one_step = true){
			status_mov <- avanzar(direccion);
			direccion <- "derecha";
			one_step <- false;
		}
		else if (direccion = "derecha" and status_mov = "libre"){
			//write name + "if 1";
			status_mov <- avanzar(direccion);
			one_step <- true;
		}
		if ((direccion = "derecha" or direccion = "izquierda") and status_mov = "bloqueado" and
			(celda_actual.grid_x = largo_mundo - 1 or celda_actual.grid_x  = 0) and one_step = true){
			//write name + "if 2";
			direccion <- "abajo";
			status_mov <- avanzar(direccion);
			one_step <- false;
		}
		else if (direccion = "abajo" and status_mov = "libre" and celda_actual.grid_x = largo_mundo - 1 and one_step = false){
			//write name + "if 3";
			direccion <- "izquierda";
		}
		else if (direccion = "abajo" and status_mov = "libre" and celda_actual.grid_x = 0 and one_step = false){
			//write name + "if 4";
			direccion <- "derecha";
			status_mov <- avanzar(direccion);
			one_step <- true;
		}
		if direccion = "izquierda" and status_mov = "libre"{
			//write name + "if 5";
			one_step <- true;
			status_mov <- avanzar(direccion);
		}
		if celda_actual.grid_x = 0 and direccion = "abajo" and status_mov = "bloqueado"{
			//write name + "if 6";
			direccion <- "derecha";
			status_mov <- "libre";
			one_step <- true;
		} 
		if verbose{
			write name + "explorar_mundo" + " " + status_mov + " " + direccion + " " + string(celda_actual.grid_x) + " " + string(largo_mundo - 1) + " " + one_step;
		}	
	}

	// Si el agente está recordando las ubicaciones donde había basura, se dirige a la primera de las ubicaciones que esté en la lista (siempre y cuando no esté vacía)
	reflex regresar_por_basura when: status_mental = "recordando" and not(ubicacion_basura = [])
	{
		if celda_actual.esta_sucia = false and cargando_basura = false{
			remove celda_actual from: ubicacion_basura;
		}
		if not(ubicacion_basura = []){
			do ir_a_celda(first(ubicacion_basura));
		}
		if (ubicacion_basura = []){
			status_mental <- "reanudando_exploracion";
		}
		if verbose{
			write name + "regresar_por_basura" + " " + status_mov + " " + status_mental + " " + direccion + " " + ubicacion_basura;
		}
			
	}
	
	
	// Si el agente llega a una celda que está sucia (tiene basura) y no está cargando basura actualmente (porque su capacidad es de 1) entonces la toma, marca
	// la celda como no-sucia y la quita de las ubicaciones de basura en memoria 
	reflex cargar_basura when: celda_actual.esta_sucia = true and cargando_basura = false
	{
		remove celda_actual from: ubicacion_basura;
		celda_actual.esta_sucia <- false;
		celda_actual.color <- #white;
		cargando_basura <- true;
	}
	// reflejo para moverse a la ubicación del bote cuando el agente está llevando basura al bote
	reflex ir_a_bote when: status_mental = "llevando_basura"
	{
		do ir_a_celda(ubicacion_bote);
		if verbose{
		write name + "ir_a_bote" + " " + status_mov + " " + status_mental + " " + direccion + " " + ubicacion_basura;
		}
		
	}
	
	// Este reflex sirve para que, una vez que el agente esté cargando basura y conozca la ubicación del bote, se dirija directamente el bote a depositarla. El agente puede
	// entrar a este estado porque se encontró la basura mientras exploraba o porque llegó a ella gracias a sus recuerdos. 
	reflex llevando_basura_al_bote when: cargando_basura = true and not(ubicacion_bote = nil) and (status_mental = "explorando" or status_mental = "recordando" )
	{
		if status_mental = "explorando" // si esa basura se la encontró mientras exploraba, guarda los datos de exploración para reanudarla después de entregar la basura
		{
			ultima_celda_exp <- celda_actual;
			ultima_direccion_exp <- direccion;
		}
		status_mental <- "llevando_basura"; // cambia su estado a "llevando basura"
	}

	// Este reflejo se usa para depositar la basura en el bote cuando el agente que está llevando basura llega a la celda del bote.
	reflex deposita_basura when: celda_actual.tiene_bote and status_mental = "llevando_basura"  
	{
			cargando_basura <- false; // suelta la basura
			basura_entregada <- basura_entregada + 1; // agrega una basura a la cantidad de entregadas
			if verbose{
				write name + "ha depositado " + basura_entregada + " montones de basura";
				write name + "Faltante " + length(ubicacion_basura);
			}	
			ask bote // le solicita al bote que incremente la cantidad de basura en su interior.
			{
				do llenado;
			}
			if ubicacion_basura = []{
				status_mental <- "explorando";
				write "=================================================================";
				write ultima_celda_exp;
				direccion <- ultima_direccion_exp;
				status_mov <- avanzar(direccion);
				
			}
			else{		
				status_mental <- "reanudando_exploracion"; //una vez entregada la basura, entra al estado de reanudar la exploración
			}
	}
	
	// este reflex reanuda la exploración, para ello se dirige a la última celda explorada y una vez ahí, establece la dirección del agente como la
	// ultima dirección tue tenía mientras exploraba. Luego hace que el agente regrese al estado de "explorando"
	reflex reinicia_ruta when: status_mental = "reanudando_exploracion"
	{
		if verbose{
				write name + "reinicia_ruta " + basura_entregada + " montones de basura";
			}
		do ir_a_celda(ultima_celda_exp);
		if celda_actual = ultima_celda_exp
		{
			status_mental <- "explorando";
			direccion <- ultima_direccion_exp;
		}
	}
	
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// A PARTIR DE AQUÍ VAN LAS ACCIONES DEL AGENTE, SOLO SE REALIZAN CUANDO SON SOLICITADAS //
	
	// Esta primer acción sirve para AVANZAR UNA CELDA en la dirección adecuada para acercarse a una celda objetivo.
	action ir_a_celda(mundo celda_objetivo)
	{
		// nuestro agente se va a mover en "L" de tan forma que siempre resuelve para la componente horizontal del movimiento y luego 
		// para la componente vertical.
		write celda_actual.grid_x;
		write celda_objetivo.grid_x;
		if celda_actual.grid_x < celda_objetivo.grid_x 
		{
			direccion <- "derecha";
			status_mov <- avanzar(direccion);
		}
		else if celda_actual.grid_x > celda_objetivo.grid_x
		{
			direccion <- "izquierda";
			status_mov <- avanzar(direccion);
		}
		else if celda_actual.grid_y < celda_objetivo.grid_y
		{
			direccion <- "abajo";
			status_mov <- avanzar(direccion);	
		}
		else if celda_actual.grid_y > celda_objetivo.grid_y
		{
			direccion <- "arriba";
			status_mov <- avanzar(direccion);	
		}
	}
	
	action avanzar(string direccion_de_mov)
	{
		string status;
		switch direccion_de_mov // selecciona una celda objetivo dependiendo de la dirección de movimiento
		{	
			match "derecha"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_x = celda_actual.grid_x + 1));}
			match "izquierda"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_x = celda_actual.grid_x - 1));}
			match "abajo"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_y = celda_actual.grid_y + 1));}
			match "arriba"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_y = celda_actual.grid_y - 1));}
		}
		
		if (celda_siguiente != nil) // si encuentra a donde moverse, se mueve y establece la nueva celda y su ubicación como actuales.
		{
			status <- "libre"; // regresa el estado "libre", indicando que el puede seguir porque si encontró objetivo.
			celda_anterior <- celda_actual;
			celda_actual <- celda_siguiente;
			location <- celda_actual.location; // establece su ubicación en la nueva celda actual
		}
		else{
			status <- "bloqueado"; // de lo contrario, indica que el camino está bloqueado.
		}
		
		// A partir de aquí se comprueba si el agente ya lleva basura mientras se mueve, y se establece la lógica para tratar
		// las celdas por donde se mueve de acuerdo con el estado de la celda y el agente, esto permite una visualización de las acciones
		// del agente durante su movimiento
		
		// si está cargando basura y la celda actual no está sucia, marcará la celda actual con azul 
		if cargando_basura = true and celda_actual.esta_sucia = false
		{
			celda_actual.color <- #darkmagenta;
		}
		// si está cargando basura pero la celda anterior tenía basura, le establece el color verde
		if cargando_basura = true and celda_anterior.esta_sucia = true
		{
			celda_anterior.color <-  #green;
		}
		// si está cargando basura y la celda anterior no tiene basura y no tiene al bote, la pone en blanco.
		else if cargando_basura = true and celda_anterior.esta_sucia = false and not(celda_anterior.tiene_bote)
		{
			celda_anterior.color <-  #white;
		}
		return status;
	}

	// aspecto base del agente
	aspect base 
	{	
		draw circle(1) color: #red;
		draw ("     " + name) color: #brown;
	}
}

// Creamos la especie carro, a la cual se le da la habilidad de moverse
species carro skills: [moving]
{	
	// los primeros dos atributos son del tipo "mundo" por lo que son en realidad del tipo "celda" y por lo tanto heredan los atributos de dicha clase.
	mundo celda_actual; // celda actual del agente (carro)
	mundo celda_siguiente; // celda objetivo, a donde se va a mover el agente
	mundo celda_anterior; // celda que el agente visitó en el paso anterior
	mundo ultima_celda_exp; //ultima celda que tocó en modo exploración
	string ultima_direccion_exp; // ultima dirección que tuvo al estar en modo exploración
	string name; // nombre del agente
	string direccion;
	string status_mental; // estado mental del agente, determina sus acciones
	string status_mov; // estado de movimiento del agente, indica si el movimiento solicitado fue posible o no
	bool cargando_basura; 
	bool verbose <- true;
	int basura_entregada <- 0;
	list<mundo> ubicacion_basura <- []; // lista de ubicaciones de la basura en el mundo
	mundo ubicacion_bote; // ubicacion del bote una vez que lo encuentre
	
	reflex end_game when: bote_lleno = true{
		
		if verbose{
		write name + "Numero final de basura recolectada: " + basura_entregada;
		}	
	}
	
	// este reflejo actualiza la percepción del mundo del agente, guarda en su memoria las ubicaciones de la basura, aunque esto solo lo puede hacer en modo exploración
	// porque si aún no reconoce el mundo, no puede saber la ubicación de la basura
	reflex actualizar_percepcion when: status_mental = "explorando"
	{
		if celda_actual.color = #green and not(celda_actual in ubicacion_basura) // si el color de la celda actual es verde (está sucia) y no está ya en la lista de ubicaciones:
		{ 
			add celda_actual to: ubicacion_basura;
			if verbose{
		write name + "¡Basura encontrada" + ubicacion_basura;
		}	
		}
		if (ubicacion_bote = nil) and celda_actual.tiene_bote // si la celda actual tiene el bote y aún no se conoce la ubicación del bote:
		{
			ubicacion_bote <- celda_actual;
			if verbose{
		write name + "¡Bote encontrado! En celda "+ "celda_actual";
		}	
		}
	}
	
	// todo agente recien creado debe ubicarse llegando al origen del mundo (o sea, la celda 0,0). Para lograrlo se mueve hacia arriba 
	// hasta llegar a una orilla del mundo y luego hacia la izquierda hasta llegar a la primer celda, una vez ahí se considera "ubicado"
	reflex busca_origen when: status_mental = "perdido" 
	{
		if status_mov = "libre" and direccion = "arriba"
		{
			status_mov <-  avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "arriba"
		{
			direccion <- "izquierda";
			status_mov <- "libre";
		}
		if status_mov = "libre" and direccion = "izquierda"
		{
			status_mov <-  avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "izquierda"
		{
			status_mental <- "ubicado";
			status_mov <- "libre";
			direccion <- "abajo";
		}		

	}
	
	// una vez que el agente está ubicado, deberá determinar el tamaño del mundo y para lograrlo realizará una rutina similar a la de ubicación
	// pero ahora se moverá hacia abajo y luego hacia la derecha hasta encontrar la esquina opuesta del mundo tras lo cuál estará familiarizado 
	// y entrará al modo de exploracion
	reflex mide_mundo when: status_mental = "ubicado"
	{
		if status_mov = "libre" and direccion = "abajo"
		{
			status_mov <-  avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "abajo"
		{
			direccion <- "derecha";
			status_mov <- "libre";
		}
		if status_mov = "libre" and direccion = "derecha"
		{
			status_mov <-  avanzar(direccion);
		}
		if status_mov = "bloqueado" and direccion = "derecha"
		{
			status_mental <- "explorando";
			status_mov <- "libre";
			direccion <- "izquierda";
		}		

	}
	
	// Lo primero que tiene que comprobar el agente al entrar en modo exploración es ver comprobar si cumple las condiciones para regresar por basura 
	// Este reflex sirve para que el agente recuerde las celdas que tienen basura, para ello tiene que estar explorando (es decir, ya familiarizado con el mundo)
	// y debe conocer la ubicación del bote y debe tener algo que recordar (la lista de ubicaciones de basura no debe estar vacía)
	reflex recordar when: status_mental = "explorando" and not(ubicacion_basura = []) and not(ubicacion_bote = nil)
	{
		// Primero guarda la celda actual (que será la del bote) y dirección de movimiento para poder reanudar la exploración una vez que haya entregado la basura. 
		ultima_celda_exp <- celda_actual; //guarda la celda actual como ultima celda explorada
		ultima_direccion_exp <- direccion; // guarda su dirección de movimiento actual como la ultima dirección antes de salir del estado "explorando"
		status_mental <- "recordando";
	}
	
	
	// Si el agente no tiene basura que recordar,  se dispone a explorar. A partir de que el agente está familiarizado ya sabe la posición en 
	// la que se encuentra y puede inferir sus coordenadas, por ello puede seguir una ruta para buscar basura o el bote. Este comportamiento se 
	// ejecutará siempre y cuando no tenga el bote ya identificado y esté cargando basura, porque si esas dos condiciones se dan simultaneamente
	// dejará de lado la exploración y procederá a dirigirse al bote
	reflex explorar_mundo when: status_mental = "explorando" 
	{
		if (direccion = "izquierda" and not(celda_actual = mundo(0)) and status_mov = "libre") or   // si no está en la esquina superior izquierda viniendo de la derecha
		(direccion = "derecha" and not(celda_actual = mundo(largo_mundo-1)) and status_mov = "libre") // si no está en la esquina superior derecha viniendo de la izquierda		
		{
			status_mov <- avanzar(direccion); // se mueve horizontalmente
		}
		else if direccion = "izquierda" and status_mov = "bloqueado" and not(celda_actual.grid_y = 0) // si llegó a la orilla izquierda del mundo
		{
			direccion <- "arriba";
			status_mov <- avanzar(direccion); // se mueve uno pa'rriba
			direccion <- "derecha";
		}

		else if direccion = "derecha" and status_mov = "bloqueado" and not(celda_actual.grid_y = 0) // si llegó a la orilla derecha del mundo
		{
			direccion <- "arriba";
			status_mov <- avanzar(direccion); //  se mueve uno pa'rriba
			direccion <- "izquierda";
		}
	}

	// Si el agente está recordando las ubicaciones donde había basura, se dirige a la primera de las ubicaciones que esté en la lista (siempre y cuando no esté vacía)
	reflex regresar_por_basura when: status_mental = "recordando" and not(ubicacion_basura = [])
	{
			do ir_a_celda(first(ubicacion_basura));
	}	
	
	// Si el agente llega a una celda que está sucia (tiene basura) y no está cargando basura actualmente (porque su capacidad es de 1) entonces la toma, marca
	// la celda como no-sucia y la quita de las ubicaciones de basura en memoria 
	reflex cargar_basura when: celda_actual.esta_sucia = true and cargando_basura = false
	{
		remove celda_actual from: ubicacion_basura;
		celda_actual.esta_sucia <- false;
		celda_actual.color <- #white;
		cargando_basura <- true;
	}
	
	// Este reflex sirve para que, una vez que el agente esté cargando basura y conozca la ubicación del bote, se dirija directamente el bote a depositarla. El agente puede
	// entrar a este estado porque se encontró la basura mientras exploraba o porque llegó a ella gracias a sus recuerdos. 
	reflex llevando_basura_al_bote when: cargando_basura = true and not(ubicacion_bote = nil) and (status_mental = "explorando" or status_mental = "recordando" )
	{
		if status_mental = "explorando" // si esa basura se la encontró mientras exploraba, guarda los datos de exploración para reanudarla después de entregar la basura
		{
			ultima_celda_exp <- celda_actual;
			ultima_direccion_exp <- direccion;
		}
		status_mental <- "llevando_basura"; // cambia su estado a "llevando basura"
	}
	
	// reflejo para moverse a la ubicación del bote cuando el agente está llevando basura al bote
	reflex ir_a_bote when: status_mental = "llevando_basura" 
	{
		do ir_a_celda(ubicacion_bote);
	}

	// Este reflejo se usa para depositar la basura en el bote cuando el agente que está llevando basura llega a la celda del bote.
	reflex deposita_basura when: celda_actual.tiene_bote and status_mental = "llevando_basura"  
	{
			cargando_basura <- false; // suelta la basura
			basura_entregada <- basura_entregada + 1; // agrega una basura a la cantidad de entregadas
			if verbose{
		write name + "ha depositado " + basura_entregada + " montones de basura";
		}	
			ask bote // le solicita al bote que incremente la cantidad de basura en su interior.
			{
				do llenado;
			}
			status_mental <- "reanudando_exploracion"; //una vez entregada la basura, entra al estado de reanudar la exploración
	}
	
	// este reflex reanuda la exploración, para ello se dirige a la última celda explorada y una vez ahí, establece la dirección del agente como la
	// ultima dirección tue tenía mientras exploraba. Luego hace que el agente regrese al estado de "explorando"
	reflex reinicia_ruta when: status_mental = "reanudando_exploracion"
	{
		do ir_a_celda(ultima_celda_exp);
		if celda_actual = ultima_celda_exp
		{
			status_mental <- "explorando";
			direccion <- ultima_direccion_exp;
		}
	}
	
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// A PARTIR DE AQUÍ VAN LAS ACCIONES DEL AGENTE, SOLO SE REALIZAN CUANDO SON SOLICITADAS //
	
	// Esta primer acción sirve para AVANZAR UNA CELDA en la dirección adecuada para acercarse a una celda objetivo.
	action ir_a_celda(mundo celda_objetivo)
	{
		// nuestro agente se va a mover en "L" de tan forma que siempre resuelve para la componente horizontal del movimiento y luego 
		// para la componente vertical. 
		if celda_actual.grid_x < celda_objetivo.grid_x 
		{
			direccion <- "derecha";
			status_mov <- avanzar(direccion);
		}
		else if celda_actual.grid_x > celda_objetivo.grid_x
		{
			direccion <- "izquierda";
			status_mov <- avanzar(direccion);
		}
		else if celda_actual.grid_y < celda_objetivo.grid_y
		{
			direccion <- "abajo";
			status_mov <- avanzar(direccion);	
		}
		else if celda_actual.grid_y > celda_objetivo.grid_y
		{
			direccion <- "arriba";
			status_mov <- avanzar(direccion);	
		}
	}
	
	// Esta es una acción general de avance en una dirección dada, el argumento es la dirección de movimiento y regresa un estado
	// de movimiento, cuando no encuentra una celda para moverse (o sea, que llegó a una orilla del mundo) indica que está bloqueado
	action avanzar(string direccion_de_mov)
	{
		string status;
		switch direccion_de_mov // selecciona una celda objetivo dependiendo de la dirección de movimiento
		{	
			match "derecha"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_x = celda_actual.grid_x + 1));}
			match "izquierda"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_x = celda_actual.grid_x - 1));}
			match "abajo"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_y = celda_actual.grid_y + 1));}
			match "arriba"{celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_y = celda_actual.grid_y - 1));}
		}
		
		if (celda_siguiente != nil) // si encuentra a donde moverse, se mueve y establece la nueva celda y su ubicación como actuales.
		{
			status <- "libre"; // regresa el estado "libre", indicando que el puede seguir porque si encontró objetivo.
			celda_anterior <- celda_actual;
			celda_actual <- celda_siguiente;
			location <- celda_actual.location; // establece su ubicación en la nueva celda actual
		}
		else
		{
			status <- "bloqueado"; // de lo contrario, indica que el camino está bloqueado.
		}
		
		// A partir de aquí se comprueba si el agente ya lleva basura mientras se mueve, y se establece la lógica para tratar
		// las celdas por donde se mueve de acuerdo con el estado de la celda y el agente, esto permite una visualización de las acciones
		// del agente durante su movimiento
		
		// si está cargando basura y la celda actual no está sucia, marcará la celda actual con azul 
		if cargando_basura = true and celda_actual.esta_sucia = false
		{
			celda_actual.color <- #deepskyblue;
		}
		// si está cargando basura pero la celda anterior tenía basura, le establece el color verde
		if cargando_basura = true and celda_anterior.esta_sucia = true
		{
			celda_anterior.color <-  #green;
		}
		// si está cargando basura y la celda anterior no tiene basura y no tiene al bote, la pone en blanco.
		else if cargando_basura = true and celda_anterior.esta_sucia = false and not(celda_anterior.tiene_bote)
		{
			celda_anterior.color <-  #white;
		}
		return status;
	}

	// aspecto base del agente
	aspect base 
	{	
		draw circle(1) color: #red;
		draw ("     " + name) color: #brown;
	}
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Creamos la especie de agente que será el bote de basura
species bote
{
	mundo celda_ubicacion; // ubicación del bote
	int cantidad_de_basura; // cantidad de basura en el bote
	int capacidad; // capacidad maxuma del bote
	image_file icono_bote <- image_file("../includes/bote_de_basura.png"); // imagen para la apareincia del bote
	
	// establecemos un reflejo del bote que comprueba si está lleno, y si lo está entonces habilita la condicón de paro de simulación
	reflex bote_a_tope
	{
		if cantidad_de_basura = capacidad
		{
			write "¡Bote lleno!";
			bote_lleno <- true;
		}
	}
	
	// se establece un acción de llenado, ésta será solicitada por otro agente para hacerle saber al bote que a entrado basura enél
	action llenado
	{
		cantidad_de_basura <- cantidad_de_basura + 1;
	}
	
	// aspecto del bote, tomamos la imagen de arriba para que la dibuje el programa
	aspect base
	{
		draw (icono_bote) size: 3;
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

experiment tarea type: gui {

	output {
		display main_display {
			grid mundo border: #blue;
			species carro aspect: base;
			species rickmovil aspect: base;
			species bote aspect: base;
		}
	}
}