/**
* Name: ECA184
* Simulación del Autómata Celular de Wolfram regla 184. 
* Author: PC-04
* Tags: 
*/


model ECA184

/* Insert your model definition here */

global{
	// primero establecemos las dimensiones del mundo y declaramos la variable para identificar las celdas basura
	int largo_mundo <- 100;
	int ancho_mundo <- 1;
	int num_carros_vecinos <- 8; // Solo se puede utililzar 4, 6 u 8 y solo toma distancia de r=1
	int num_ciclos <- int(largo_mundo/2) + 1;
	int cont_ciclos <- 0;
	
	float prob_densidad <- 0.5;
	int num_coches <- int(prob_densidad*largo_mundo);
	
	list<carretera> ubicacion_autos <- [];
	list atascos <- [];
	map atascos_dict <- [];
	
	bool update <- true;
	
	init{
		create coche number:num_coches{
			celda_actual <- one_of(carretera where (not each.celda_ocupada));
			celda_actual.color <- #green;
			celda_actual.celda_ocupada <- true;
			location <- celda_actual.location;
			add celda_actual to: ubicacion_autos;
			ubicacion_autos <- ubicacion_autos sort_by (each);
			//write ubicacion_autos;
		}
		do jam();
	}
	reflex when: cont_ciclos >= num_ciclos{
		do pause;
	}
	reflex get_jam{
		do jam();
	}
	
	action jam{
		int contador <- 0;
		list aux <- [];
		list mundo <- [];
		
		loop c over: carretera{
			if c.celda_ocupada{
				contador <- contador +1;
				add 1 to: mundo;
			}
			if not c.celda_ocupada{
				add contador to: aux;
				add 0 to: mundo;
				contador <- 0;
			}
			if c.grid_x = (largo_mundo-1) and (contador != 0) and (aux[0] != 0){
				aux[0] <- int(aux[0]) + contador;
			}
			if c.grid_x = (largo_mundo-1) and (contador != 0) and (aux[0] = 0){
				add contador to:aux;
			}
		}
		loop a over: aux{
			if a != 0{
				add a to: atascos;
			}
		}
		//write "[Jams]: " + atascos;
		atascos_dict <- (atascos frequency_of each);
		//write "[Jams frecuencia]: " + atascos_dict;
		atascos <- [];
	}
}

grid carretera width: largo_mundo height: ancho_mundo neighbors: num_carros_vecinos {
	bool celda_ocupada <- false;
	bool estaba_ocupada <- false;
	reflex limpiar_celdas_anteriores{
		estaba_ocupada <- false;
	}
}

species coche skills: [moving]{
	carretera celda_actual; 
	carretera celda_siguiente;
	carretera celda_anterior;
	
	image_file icono_bote <- image_file("../includes/bote_de_basura.png");
	
	reflex actualizar_percepcion{
		celda_siguiente <- one_of(celda_actual.neighbors where(each.grid_x = celda_actual.grid_x + 1));
		if celda_siguiente = nil{
			celda_siguiente <- carretera(0);
		}
		//write "Celda actual: " + celda_actual + "  Celda siguiente: " + celda_siguiente + " esta: " +celda_siguiente.celda_ocupada + " estaba: " +celda_siguiente.estaba_ocupada;
		if celda_siguiente.celda_ocupada or celda_siguiente.estaba_ocupada{
			celda_siguiente <- celda_actual;
		}
	}
	reflex avanzar{
		celda_actual.color <- #white;
		celda_siguiente.color <- #green;
		celda_actual.estaba_ocupada <- true;
		celda_actual.celda_ocupada <- false;
		celda_siguiente.celda_ocupada <- true;
		
		celda_anterior <- celda_actual;
		celda_actual <- celda_siguiente;
	}
	
	aspect{
		draw square(1) color: #red;
	}
}


experiment Trafico type: gui {
	parameter "Densidad de doches" var: prob_densidad min: 0.0 max: 0.99;
	
	output {
		display main_display {
			//grid carretera border: #blue;
			grid carretera border: #blue position: { 0, 0.5 } size: {1,1/largo_mundo};
			species coche;
		}
	}
	reflex get_jam{
		do jam();
	}
	
	action jam{
		int contador <- 0;
		list aux <- [];
		list mundo <- [];
		
		loop c over: carretera{
			//write "" + c + " " + c.celda_ocupada;
			if c.celda_ocupada{
				contador <- contador +1;
				add 1 to: mundo;
			}
			if not c.celda_ocupada{
				add contador to: aux;
				add 0 to: mundo;
				contador <- 0;
			}
			if c.grid_x = (largo_mundo-1) and (contador != 0) and (aux[0] != 0){
				aux[0] <- int(aux[0]) + contador;
			}
			if c.grid_x = (largo_mundo-1) and (contador != 0) and (aux[0] = 0){
				add contador to:aux;
			}
		}
		loop a over: aux{
			if a != 0{
				add a to: atascos;
			}
		}
		write "[Jams]: " + mundo;
		cont_ciclos <- cont_ciclos + 1;
		//write "[Jams]: " + atascos;
		atascos_dict <- (atascos frequency_of each);
		//write "[Jams frecuencia]: " + atascos_dict;
		atascos <- [];
	}
}