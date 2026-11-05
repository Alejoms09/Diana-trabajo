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
System.out.println(reserva);
try {
    new ReservaBuilder()
        .fecha(java.time.LocalDate.now().plusDays(7))
        .horaInicio(java.time.LocalTime.of(14, 0))
        .duracionHoras(2).cantidadPersonas(4)
        .sala(new Sala("B", "Sala B", 4)).build();
    throw new AssertionError("Se aceptó una reserva sin estudiante.");
} catch (IllegalStateException ex) {
    System.out.println(ex.getMessage());
}
try {
    new ReservaBuilder()
        .estudiante(new Estudiante("E001", "Laura"))
        .fecha(java.time.LocalDate.now().plusDays(7))
        .horaInicio(java.time.LocalTime.of(14, 0))
        .duracionHoras(2).cantidadPersonas(5)
        .sala(new Sala("B", "Sala B", 4)).build();
    throw new AssertionError("Se aceptó capacidad insuficiente.");
} catch (IllegalStateException ex) {
    System.out.println(ex.getMessage());
}
}
}
