package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class Main {
public static void main(String[] args) {
RepositorioSalas salas = new RepositorioSalasMemoria();
RepositorioReservasMemoria reservas = new RepositorioReservasMemoria();
ReservaFacade fachada = new ReservaFacade(salas, reservas);
Reserva reserva = fachada.realizarReserva(
    new Estudiante("E001", "Laura"), LocalDate.now().plusDays(7),
    LocalTime.of(14, 0), 2, 4, new SeleccionPorCapacidad()).orElseThrow();
System.out.println(reserva);
System.out.println("Reservas registradas: " + reservas.obtenerTodas().size());
if (fachada.realizarReserva(
    new Estudiante("E003", "Camila"), LocalDate.now().plusDays(9),
    LocalTime.of(9, 0), 2, 10, new SeleccionPorCapacidad()).isPresent()) {
    throw new AssertionError("Se creó una reserva para diez personas.");
}
if (reservas.obtenerTodas().size() != 1 || !"Confirmada".equals(reserva.getNombreEstado())) {
    throw new AssertionError("El registro o la confirmación fallaron.");
}
}
}
