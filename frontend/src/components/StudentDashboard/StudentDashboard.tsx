import React from 'react';
import { BookOpen, Users } from 'lucide-react';
import CharacterCard from '../CharacterCard/CharacterCard';

interface StudentDashboardProps {
  onCharacterSelect: (character: 'Teo' | 'Josefina') => void;
}

const StudentDashboard: React.FC<StudentDashboardProps> = ({ onCharacterSelect }) => {
  

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#E3F2FD] via-[#BBDEFB] to-[#90CAF9] pt-20 pb-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="text-center mb-12">
          <div className="w-16 h-16 bg-gradient-to-br from-[#1E88E5] to-[#42A5F5] rounded-full flex items-center justify-center mx-auto mb-6">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-[#0D47A1] mb-4">
            Bienvenido al Chat Educativo
          </h1>
          <p className="text-lg text-[#37474F] max-w-2xl mx-auto">
            Conversa con Teo y Josefina para practicar y mejorar tus habilidades de comunicación. 
            ¡Cada conversación es una oportunidad de aprender!
          </p>
        </div>

        {/* Character Selection */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-3 mb-8">
            <Users className="w-6 h-6 text-[#1E88E5]" />
            <h2 className="text-2xl font-bold text-[#0D47A1]">
              Elige con quién quieres conversar
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <CharacterCard
              name="Teo"
              age={9}
              grade="4º Básico"
              description="Teo tiene dificultades en lectura y escritura, y a veces evita las tareas de lenguaje. Responde mejor cuando recibe apoyo visual y ejemplos concretos."
              interests={['Dibujos', 'Colores', 'Juegos visuales']}
              // 4. Llama a la función del componente padre al hacer clic
              onClick={() => onCharacterSelect('Teo')}
            />

            <CharacterCard
              name="Josefina"
              age={15}
              grade="1º Medio"
              description="Josefina tiene dificultades intelectuales leves y es tímida. Aprende mejor con ejemplos concretos y disfruta de actividades relacionadas con sus intereses."
              interests={['Música', 'Fútbol', 'Ejemplos prácticos']}
              onClick={() => onCharacterSelect('Josefina')}
            />
          </div>
        </div>

        {/* Tips Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 max-w-4xl mx-auto border border-blue-200">
          <h3 className="text-lg font-semibold text-[#0D47A1] mb-4">
            💡 Consejos para una mejor conversación
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-[#37474F]">
            <div className="space-y-2">
              <p><strong>Con Teo:</strong></p>
              <ul className="space-y-1 pl-4">
                <li>• Usa ejemplos visuales y concretos</li>
                <li>• Sé paciente con las respuestas</li>
                <li>• Menciona colores y formas</li>
              </ul>
            </div>
            <div className="space-y-2">
              <p><strong>Con Josefina:</strong></p>
              <ul className="space-y-1 pl-4">
                <li>• Conecta con música y deportes</li>
                <li>• Usa ejemplos de la vida real</li>
                <li>• Dale tiempo para procesar</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;