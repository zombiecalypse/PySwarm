#ifndef PY_SWARM_H
#define PY_SWARM_H

#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <vector>
typedef boost::numeric::ublas::c_vector<double, 3> vec3;
typedef boost::numeric::ublas::zero_vector<double> zero_vec3;
typedef boost::numeric::ublas::unit_vector<double> unit_vec3;
typedef vec3 position_v;
typedef vec3 velocity_v;
typedef vec3 force_v;

class VecBuilder {
	public:
		double x_,y_,z_;
		VecBuilder& x(double _x) { x_ = _x; return *this; }
		VecBuilder& y(double _y) { y_ = _y; return *this; }
		VecBuilder& z(double _z) { z_ = _z; return *this; }
		operator vec3();
};

class Swarm;
class SwarmElement;
class SwarmElementBuilder {
	friend class SwarmElement;
	position_v pos;
	velocity_v vel;
	double m;
	public:
		SwarmElementBuilder();
		SwarmElementBuilder& position(position_v p) {
			pos = p;
			return *this;
		}

		SwarmElementBuilder& velocity(position_v v) {
			vel = v;
			return *this;
		}

		SwarmElementBuilder& mass(double _m) {
			m = _m;
			return *this;
		}
};

class SwarmElement {
	const double POSITION_ATTRACTION() { return 1.0; }
	const double VELOCITY_ATTRACTION() { return 1.0; }
	const double PUSH_STRENGTH() { return 10; }
	const double PUSH_RADIUS() { return 10; }

	friend class Swarm;
	position_v pos;
	velocity_v vel;
	velocity_v new_vel;
	double m;

	void assume_similar_position(position_v);
	void assume_similar_velocity(velocity_v);
	void keep_distance(Swarm&);
	public:
		SwarmElement(const SwarmElementBuilder&);
		SwarmElement();
		position_v position() const { return pos; }
		velocity_v velocity() const { return vel; }
		double mass() const { return m; }
		void accelerate(force_v);
		void commit();
};

std::ostream& operator<<(std::ostream& out, const SwarmElement& se) {
	return out 
		<< "SwarmElement("
		<< "pos=" << se.position() << ", "
		<< "vel=" << se.velocity() << ", "
		<< "m="   << se.mass() << ")";
}

class Swarm {
	friend class SwarmElement;

	public:
		std::vector<SwarmElement> elements;
		void step(); 
		SwarmElement operator[](int n) { return elements[n]; }
		void add(SwarmElement e) { elements.push_back(e); }
		void add(position_v, velocity_v);
		void add(position_v);
		void add_random();
};

#endif // PY_SWARM_H
