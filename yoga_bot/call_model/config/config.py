MODEL_NAME = 'google/gemma-2b-it'

PROMPT = """You are a fabulous yoga teacher. Please generate a yoga class ensuring that the flow between poses is natural for humans and they do not get hurt. Make sure the generated yoga style is """

VINYASA_EXAMPLE = """<h3 align="center"> Vinyasa Flow Yoga Class </h3>
		<h3 align="center"> Theme: Embrace the Flow </h3>
		<h3 align="center"> Duration: 60 minutes </h3>
		<h3 align="center"> Level: All levels (modifications offered throughout) </h3>
		<h3 align="center"> Props: Yoga mat (optional block) </h3>
		<h3 align="center"> Opening: </h3>
		<h4 align="center"> Begin seated in a comfortable position, closing your eyes. Take a few deep breaths in and out through your nose, grounding yourself to the mat.
			Set an intention for your practice. Perhaps it's to cultivate gratitude, find inner peace, or build strength and flexibility. </h4>
		<h3 align="center"> Warm-Up: </h3>
		<h4 align="center"> Cat-Cow Pose: Begin on all fours, wrists under shoulders and knees under hips. Inhale, dropping the belly and lifting the gaze. Exhale, rounding the spine and tucking the chin. Repeat 5-10 times, flowing with your breath. </h4>
		<h4 align="center"> Downward-Facing Dog: From all fours, tuck your toes and lift your hips up and back.  Pedal your heels gently and find length in your spine. Hold for 5 breaths. </h4>
		<h4 align="center"> Sun Salutations A & B: Flow through 3-5 rounds of each, warming up the entire body and linking breath with movement. </h4>
		<h3 align="center"> Standing Sequence: </h3>
		<h4 align="center"> Warrior II: Step your right foot forward, bend your right knee, and extend your arms out to the sides. Gaze over your right fingertips. Hold for 5 breaths. Repeat on the left side. </h4>
		<h4 align="center"> Triangle Pose: From Warrior II, straighten your front leg, hinge at the hips, and reach your front hand down to your shin or the floor. Extend your back arm towards the sky. Hold for 5 breaths. Repeat on the left side. </h4>
		<h4 align="center"> Half Moon Pose: From Triangle Pose, bring your front hand to the floor or a block. Lift your back leg and open your hips, reaching your back arm towards the sky. Gaze up or straight ahead. Hold for 3 breaths. Repeat on the left side. </h4>
        <h3 align="center"> Balancing Sequence: </h3>
		<h4 align="center"> Tree Pose: Stand on one leg, placing the sole of your other foot on your inner thigh or calf. Bring your hands to heart center or reach them overhead. Hold for 5 breaths. Repeat on the other side. </h4>
		<h4 align="center"> Dancer's Pose: Stand on one leg, kick your other foot back, and grab the ankle with your hand. Reach your opposite arm forward. Lean forward and lift your back leg, gazing forward. Hold for 3 breaths. Repeat on the other side. </h4>
        <h3 align="center"> Cool-Down: </h3>
		<h4 align="center"> Seated Forward Fold: Sit with your legs extended. Hinge at the hips and fold forward, reaching for your toes or shins. Relax your neck and shoulders. Hold for 5 breaths. </h4>
		<h4 align="center"> Reclining Twist: Lie on your back and hug your knees to your chest. Gently lower your knees to the right, keeping your shoulders grounded. Extend your left arm out to the side. Gaze over your left shoulder. Hold for 5 breaths. Repeat on the other side. </h4>
		<h3 align="center"> Savasana: </h3>
		<h4 align="center"> Lie on your back with your arms and legs extended. Close your eyes and relax your entire body. Stay here for 5-10 minutes, allowing the benefits of your practice to sink in. </h4>
		<h3 align="center"> Closing: </h3>
		<h4 align="center"> Gently roll to your right side and slowly come to a seated position. Take a moment to reflect on your practice and express gratitude for your body's ability to move and flow. </h4>
		<h3 align="center"> Namaste </h3>"""

YIN_EXAMPLE = """Welcome to our Yin yoga session. Today, we'll focus on deep stretches, holding poses for 3-5 minutes to release tension and increase flexibility. Remember, Yin is about finding stillness and surrender. Listen to your body, breathe deeply, and let go.

Let's begin by setting an intention for our practice. What do you want to cultivate today? Peace? Calm? Letting go? Hold your intention in your heart as we move through our practice.

Warm-Up:

Butterfly Pose (Baddha Konasana): Sit with the soles of your feet together, letting your knees fall open. Gently fold forward, resting your forehead on a block or your hands. (3 minutes)
Sequence:

Child's Pose (Balasana): Kneel with your big toes touching, knees wide. Extend your arms forward, resting your forehead on the mat. (5 minutes)

Dangling Pose (Uttanasana Variation): Stand with feet hip-width apart. Fold forward, letting your head and arms hang heavy. Bend your knees as needed. (3 minutes)

Caterpillar Pose (Paschimottanasana): Sit with legs extended forward. Fold over your legs, resting your forehead on a block or your hands. (5 minutes)

Supported Bridge Pose (Setu Bandha Sarvangasana): Lie on your back, knees bent, feet flat on the floor. Place a block under your sacrum (the bony part at the base of your spine). Relax your arms by your sides. (5 minutes)

Supported Reclined Twist (Supta Matsyendrasana): Lie on your back, knees bent. Gently lower your knees to the right, placing a block or blanket under them for support. Extend your arms out to the sides. Turn your head to the left. (3 minutes on each side)

Sphinx Pose (Salamba Bhujangasana): Lie on your stomach, forearms on the floor, elbows under shoulders. Lift your chest and head, keeping your hips and thighs on the ground. (3 minutes)

Cool-Down:

Savasana (Corpse Pose): Lie on your back, arms by your sides, palms facing up. Close your eyes and relax your entire body. (5-10 minutes)
Closing:

Gently bring movement back into your body by wiggling your fingers and toes. Slowly roll onto your side, taking a few breaths before coming to a seated position. Take a moment to acknowledge the stillness you've cultivated. Namaste.
"""

POWER_EXAMPLE = """Warm-Up (5 minutes):

Gentle neck rolls and shoulder shrugs
Cat-Cow Pose (Marjaryasana-Bitilasana): 5-10 rounds
Downward-Facing Dog (Adho Mukha Svanasana): Hold for 5 breaths
Plank Pose (Phalakasana): Hold for 30 seconds
Child's Pose (Balasana): Rest for a few breaths
Sun Salutations (Surya Namaskar A & B):

3 rounds of Surya Namaskar A
2 rounds of Surya Namaskar B
Standing Poses (15 minutes):

Warrior I (Virabhadrasana I): Hold each side for 5 breaths
Warrior II (Virabhadrasana II): Hold each side for 5 breaths
Reverse Warrior (Viparita Virabhadrasana): Hold each side for 5 breaths
Triangle Pose (Trikonasana): Hold each side for 5 breaths
Half Moon Pose (Ardha Chandrasana): Hold each side for 3 breaths (optional for beginners)
Balancing Poses (5 minutes):

Tree Pose (Vrksasana): Hold each side for 5 breaths
Warrior III (Virabhadrasana III): Hold for 3 breaths on each side (optional for beginners)
Core Work (5 minutes):

Boat Pose (Navasana): Hold for 30 seconds
Forearm Plank: Hold for 30 seconds
Side Plank (Vasisthasana): Hold each side for 30 seconds
Cool Down (10 minutes):

Seated forward fold (Paschimottanasana): Hold for 1 minute
Reclined twist (Supta Matsyendrasana): Hold each side for 1 minute
Legs up the wall (Viparita Karani): Rest for 5 minutes
Savasana (Corpse Pose): Final relaxation for 5 minutes"""
