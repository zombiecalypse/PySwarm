#include "python_swarm.h"
#include <boost/python.hpp>
#include <boost/accumulators/statistics/mean.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/accumulators.hpp>

#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp>
using namespace std;
const double dt = 0.1;

VecBuilder::operator vec3() {
	vec3 e;
	e(0) = x_;
	e(1) = y_;
	e(2) = z_;
	return e;
}

SwarmElementBuilder::SwarmElementBuilder() :
	pos(zero_vec3(3)),
	vel(zero_vec3(3)),
	m(1) {}
SwarmElement::SwarmElement(const SwarmElementBuilder& b) :
	pos(b.pos),
	vel(b.vel),
	new_vel(b.vel),
	m(b.m) { }
SwarmElement::SwarmElement() : 
	pos(zero_vec3(3)), 
	vel(zero_vec3(3)),
	new_vel(zero_vec3(3)),
	m(1) { }

void SwarmElement::accelerate(force_v f) {
	new_vel += f*(dt/m);
}

void SwarmElement::commit() {
	pos += vel * dt;
	vel = new_vel;
}

void SwarmElement::assume_similar_position(position_v p) {
	vec3 d = p - pos;
	accelerate(d*POSITION_ATTRACTION());
}

void SwarmElement::assume_similar_velocity(velocity_v v) {
	vec3 d = v - vel;
	accelerate(d*VELOCITY_ATTRACTION());
}

void SwarmElement::keep_distance(Swarm& s) {
	for (SwarmElement& e : s.elements) {
		if (&e == this) continue;
		vec3 d = e.position() - pos;
		if (norm_2(d) < PUSH_RADIUS()) {
			accelerate(PUSH_STRENGTH() * d);
		}
	}
}

void Swarm::step() {
	using namespace boost::accumulators;
	accumulator_set<position_v, stats<tag::mean> > pos_mean;
	accumulator_set<velocity_v, stats<tag::mean> > vel_mean;
	for (SwarmElement& e : elements) {
		pos_mean(e.position());
		vel_mean(e.velocity());
	}
}

void Swarm::add(position_v p, velocity_v v) {
	SwarmElement e = SwarmElementBuilder()
				.position(p)
				.velocity(v);
	add(e);
}

void Swarm::add(position_v p) {
	SwarmElement e = SwarmElementBuilder()
				.position(p);
	add(e);
}

static boost::mt19937 rng;
static boost::normal_distribution<> normal_dist;
static boost::variate_generator<boost::mt19937&, boost::normal_distribution<> > normal(rng, normal_dist);
void Swarm::add_random() {
	SwarmElement e = SwarmElementBuilder()
				.position(VecBuilder()
					.x(normal())
					.y(normal())
					.z(normal()))
				.velocity(VecBuilder()
					.x(normal())
					.y(normal())
					.z(normal()));
	add(e);
					
}
int main() {
	Swarm swarm;
	swarm.add_random();
	for (SwarmElement& el : swarm.elements) {
		cout << el << endl;
	}
}

using namespace boost::python;

template <class V>
struct Vec3ToTupleConvert {
	static PyObject* convert(const V& v) {
		return incref(make_tuple(v[0],v[1],v[2]).ptr());
	}
};


BOOST_PYTHON_MODULE(pyswarm) {
	to_python_converter<vec3, Vec3ToTupleConvert<vec3> >();
	class_<Swarm>("Swarm")
		.def("add_random", &Swarm::add_random)
		.def("__getitem__", &Swarm::operator[])
		;
	class_<SwarmElement>("SwarmElement")
		.def("position", &SwarmElement::position)
		.def("velocity", &SwarmElement::velocity)
		;
}
