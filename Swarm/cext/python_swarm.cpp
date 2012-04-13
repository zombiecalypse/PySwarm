#include "python_swarm.h"
#include <math.h>
#include <boost/python.hpp>
#include <boost/accumulators/statistics/mean.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/accumulators.hpp>

#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp>

#include <sstream>
using namespace std;
const double dt = 0.1;

VecBuilder::operator vec3() {
	vec3 e;
	e(0) = x_;
	e(1) = y_;
	e(2) = z_;
	return e;
}

bool valid(vec3 p) {
	using std::isnan;
	return !(isnan(p(0)) || isnan(p(1)) || isnan(p(2)));
}

SwarmElementBuilder::SwarmElementBuilder() :
	pos(zero_vec3(3)),
	vel(zero_vec3(3)),
	m(1) {}
SwarmElement::SwarmElement(const SwarmElementBuilder& b) :
	pos(b.pos),
	vel(b.vel),
	new_vel(b.vel),
	m(b.m) { 
	assert(m > 0);
	assert(valid(pos));
	assert(valid(vel));
}
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
	vel = (SPEED()/norm_2(new_vel)) * new_vel;
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
	vec3 pos_sum;
	vec3 vel_sum;
	const unsigned n = elements.size();
	for (SwarmElement& e : elements) {
		pos_sum += e.position() / n;
		vel_sum += e.velocity() / n;
	}
	const vec3 pos_mean =  pos_sum;
	const vec3 vel_mean =  vel_sum;
	for (SwarmElement& e : elements) {
		e.assume_similar_position(pos_mean);
		e.assume_similar_velocity(vel_mean);
		e.keep_distance(*this);
	}
	for (SwarmElement& e : elements) {
		e.commit();
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

std::string SwarmElement::str() const {
	stringstream s;
	s << *this;
	return s.str();
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
		.add_property("elements", range(&Swarm::el_begin, &Swarm::el_end))
		.def("add_random", &Swarm::add_random)
		.def("step", &Swarm::step)
		.def("__getitem__", &Swarm::operator[], return_value_policy<reference_existing_object>())
		;
	class_<SwarmElement>("SwarmElement")
		.def_readonly("position", &SwarmElement::position)
		.def_readonly("velocity", &SwarmElement::velocity)
		.def("__str__", &SwarmElement::str)
		;
}
