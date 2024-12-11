/**
* Name: TCA2Dinterseccion
* Based on the internal empty template. 
* Author: PC-04
* Tags: 
*/

model TCA2Dinterseccion

global{
	int num_carros_vecinos 			<- 8; // Solo se puede utililzar 4, 6 u 8 y solo toma distancia de r=1
	// primero establecemos las dimensiones del mundo y declaramos la variable para identificar las celdas basura
	int ancho_mundo 				<- 57;  // este es i/x
	int largo_mundo 				<- 57;  // este es j/y
	
	// para hacer los vecinarios no habitables del grid
	int max_mod_horizontal 			<- 4; // Disminuye en 1
	int max_mod_vertical 			<- 7; // Disminuye en 1
	
	float prob_densidad_horizontal 	<- 0.1; 
	float prob_densidad_vertical   	<- 0.4;
	int num_coches_horizontal		<- int((ancho_mundo - floor(largo_mundo / (max_mod_vertical + 1))) * floor(ancho_mundo / (max_mod_horizontal + 1)) * prob_densidad_horizontal);
	int num_coches_vertical   		<- int((largo_mundo - floor(ancho_mundo / (max_mod_horizontal + 1))) * floor(largo_mundo / (max_mod_vertical + 1)) * prob_densidad_vertical);
	
	list<cuadricula> ubicacion_autos <- [];
	
	init{
		if num_coches_horizontal = 0{
			num_coches_horizontal <- 1;
		}
		if num_coches_vertical = 0{
			num_coches_vertical <- 1;
		}
		max_mod_horizontal <- max_mod_horizontal + 1; // Disminuye en 1
		max_mod_vertical <- max_mod_vertical + 1; // Disminuye en 1
		loop i from: 0 to: ancho_mundo-1{
			loop j from: 0 to: largo_mundo-1{
				int coord <- i*largo_mundo + j;
				
				if i mod max_mod_horizontal != (max_mod_horizontal-1) and j mod max_mod_vertical != (max_mod_vertical-1){
					cuadricula[coord].color <- #grey;
					cuadricula[coord].celda_ocupada <- true;
				}
				
				if i mod max_mod_horizontal = (max_mod_horizontal-1) and j mod max_mod_vertical = (max_mod_vertical-1){
					cuadricula[coord].semaforo <- true;
				}
				
				if i mod max_mod_horizontal = (max_mod_horizontal-1) and not cuadricula[coord].celda_ocupada and not cuadricula[coord].semaforo{
					cuadricula[coord].horizontal <- true;
				}
				if j mod max_mod_vertical = (max_mod_vertical-1) and not cuadricula[coord].celda_ocupada and not cuadricula[coord].semaforo{
					cuadricula[coord].vertical <- true;
				}
			}
		}
		create coche_horizontal number:num_coches_horizontal{
			celda_actual <- one_of(cuadricula where (not each.celda_ocupada and not each.semaforo and each.horizontal));
			celda_actual.color <- #cadetblue;
			celda_actual.celda_ocupada <- true;
			location <- celda_actual.location;
			add celda_actual to: ubicacion_autos;
			ubicacion_autos <- ubicacion_autos sort_by (each);
		}
		create coche_vertical number:num_coches_vertical{
			celda_actual <- one_of(cuadricula where (not each.celda_ocupada and not each.semaforo and each.vertical));
			celda_actual.color <- #burlywood;
			celda_actual.celda_ocupada <- true;
			location <- celda_actual.location;
			add celda_actual to: ubicacion_autos;
			ubicacion_autos <- ubicacion_autos sort_by (each);
		}
	}
}

grid cuadricula width: largo_mundo height: ancho_mundo neighbors: num_carros_vecinos {
	bool celda_ocupada <- false;
	bool estaba_ocupada <- false;
	bool semaforo <- false;
	bool horizontal <- false;
	bool vertical <- false;
	
	reflex limpiar_celdas_anteriores{
		estaba_ocupada <- false;
	}
}

species coche_horizontal skills: [moving]{
	cuadricula celda_actual; 
	cuadricula celda_siguiente;
	cuadricula celda_anterior;
	cuadricula vecino_derecho;
	
	reflex actualizar_percepcion{
		do get_celda_siguiente();
		vecino_derecho <- cuadricula(((celda_actual.grid_y+1) * largo_mundo) + (celda_actual.grid_x + 2));
		if vecino_derecho = nil{
			vecino_derecho <- cuadricula(((celda_actual.grid_y+1) * largo_mundo));			
		}
		if abs(vecino_derecho.grid_y - celda_actual.grid_y) > 1{
			vecino_derecho <- cuadricula(((celda_actual.grid_y) * largo_mundo) + (celda_actual.grid_x + 2));
		}
		if celda_siguiente.celda_ocupada = true or celda_siguiente.estaba_ocupada = true{
			celda_siguiente <- celda_actual;
		}
	}
	
	reflex avanzar{
		celda_actual.estaba_ocupada <- true;
		celda_actual.celda_ocupada <- false;
		celda_siguiente.celda_ocupada <- true;
		
		celda_anterior <- celda_actual;
		celda_actual <- celda_siguiente;
		//do get_celda_siguiente();
		
		celda_anterior.color <- #white;
		celda_actual.color <- #cadetblue;
	}
	
	action get_celda_siguiente{
		celda_siguiente <- one_of(celda_actual.neighbors where (each.grid_x = celda_actual.grid_x + 1 and each.grid_y = celda_actual.grid_y));
		if celda_siguiente = nil{
			int y <- celda_actual.grid_y;
			celda_siguiente <- cuadricula(y*largo_mundo);
		}
	}
}

species coche_vertical skills: [moving]{
	cuadricula celda_actual; 
	cuadricula celda_siguiente;
	cuadricula celda_anterior;
	cuadricula vecino_derecho;
	
	reflex actualizar_percepcion{
		do get_celda_siguiente();
		vecino_derecho <- cuadricula((celda_siguiente.grid_y + 1)*ancho_mundo + celda_actual.grid_x - 1);
		if vecino_derecho = nil{
			vecino_derecho <- cuadricula(celda_actual.grid_x - 1);
		}
		if celda_siguiente.celda_ocupada = true or celda_siguiente.estaba_ocupada = true{
			celda_siguiente <- celda_actual;
		}
	}
	
	reflex avanzar{
		celda_actual.estaba_ocupada <- true;
		celda_actual.celda_ocupada <- false;
		celda_siguiente.celda_ocupada <- true;
		
		celda_anterior <- celda_actual;
		celda_actual <- celda_siguiente;
		//do get_celda_siguiente();
		
		celda_anterior.color <- #white;
		celda_actual.color <- #burlywood;
	}
	
	action get_celda_siguiente{
		celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_y = celda_actual.grid_y + 1 and each.grid_x = celda_actual.grid_x));
		if celda_siguiente = nil{
			int x <- celda_actual.grid_x;
			celda_siguiente <- cuadricula(x);
		}
	}
}
	
experiment Trafico type: gui {
	output {
		display main_display {
			grid cuadricula border: #blue;
			species coche_horizontal;
		}
	}
}
