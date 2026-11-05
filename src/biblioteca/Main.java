package biblioteca;


public class Main {
public static void main(String[] args) {
Reserva reserva = new ReservaBuilder()
.estudiante(new Estudiante("E001", "Laura"))
.fecha(java.time.LocalDate.now().plusDays(7))
.horaInicio(java.time.LocalTime.of(14, 0))
.duracionHoras(2)
.cantidadPersonas(4)
.sala(new Sala("B", "Sala B", 4))
.build();
reserva.agregarObservador(new NotificadorEstudiante());
reserva.agregarObservador(new RegistroEventos());
System.out.println(reserva);
reserva.confirmar();
System.out.println(reserva);
reserva.cancelar();
System.out.println(reserva);
try {
    reserva.confirmar();
    throw new AssertionError("Se confirmó una reserva cancelada.");
} catch (IllegalStateException ex) {
    System.out.println("Operación rechazada: " + ex.getMessage());
}
Reserva otra = new ReservaBuilder()
.estudiante(new Estudiante("E004", "Samuel"))
.fecha(java.time.LocalDate.now().plusDays(7))
.horaInicio(java.time.LocalTime.of(14, 0))
.duracionHoras(2)
.cantidadPersonas(2)
.sala(new Sala("A", "Sala A", 2))
.build();
otra.agregarObservador(new NotificadorEstudiante());
otra.agregarObservador(new RegistroEventos());
otra.confirmar();
System.out.println(otra);
otra.finalizar();
System.out.println(otra);
try {
    otra.cancelar();
    throw new AssertionError("Se canceló una reserva finalizada.");
} catch (IllegalStateException ex) {
    System.out.println("Operación rechazada: " + ex.getMessage());
}
}
}
