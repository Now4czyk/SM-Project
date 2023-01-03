clear all; close all; clc;

% Odczytanie oraz sparsowanie danych
data = dlmread('data.csv', ',', 2, 0);
time_vec = data(:,1); 
output = data(:,2);
offset = output(1);
output = output - output(1); % normalizacja(wartość równa 0)

% Wykreślenie odpowiedzi skokowej
plot(time_vec, output, 'g');
title("Dane znormalizowanego modelu, wypełnienie PMW 100%");
xlabel("Czas (s)");
ylabel("Temperatura (C)");
xlim([0 max(time_vec)]);

% Estymowane tf
k = 37.75;
T = 246.6;
T0 = 14.83;
estimated_model = tf([k], [T 1], 'InputDelay', T0);
hold on;
step(estimated_model);
legend("Rzeczywista odpowiedź skokowa", "Estymowana odpowiedź skokowa", 'Location', 'southeast');

% PID w simulinku
desired_temperature = 50;
sim('PID.slx')