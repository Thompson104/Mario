// Generated by gencpp from file gripper_driver/motor_state.msg
// DO NOT EDIT!


#ifndef GRIPPER_DRIVER_MESSAGE_MOTOR_STATE_H
#define GRIPPER_DRIVER_MESSAGE_MOTOR_STATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace gripper_driver
{
template <class ContainerAllocator>
struct motor_state_
{
  typedef motor_state_<ContainerAllocator> Type;

  motor_state_()
    : angle(0.0)
    , load(0.0)  {
    }
  motor_state_(const ContainerAllocator& _alloc)
    : angle(0.0)
    , load(0.0)  {
  (void)_alloc;
    }



   typedef float _angle_type;
  _angle_type angle;

   typedef float _load_type;
  _load_type load;




  typedef boost::shared_ptr< ::gripper_driver::motor_state_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::gripper_driver::motor_state_<ContainerAllocator> const> ConstPtr;

}; // struct motor_state_

typedef ::gripper_driver::motor_state_<std::allocator<void> > motor_state;

typedef boost::shared_ptr< ::gripper_driver::motor_state > motor_statePtr;
typedef boost::shared_ptr< ::gripper_driver::motor_state const> motor_stateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::gripper_driver::motor_state_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::gripper_driver::motor_state_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace gripper_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'gripper_driver': ['/home/apc16/apc_2016/mario_catkin_workspace/stowing/src/gripper_driver/msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::gripper_driver::motor_state_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::gripper_driver::motor_state_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gripper_driver::motor_state_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gripper_driver::motor_state_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gripper_driver::motor_state_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gripper_driver::motor_state_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::gripper_driver::motor_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "821acdedeefedb4e32bbd235e52cfd8f";
  }

  static const char* value(const ::gripper_driver::motor_state_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x821acdedeefedb4eULL;
  static const uint64_t static_value2 = 0x32bbd235e52cfd8fULL;
};

template<class ContainerAllocator>
struct DataType< ::gripper_driver::motor_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "gripper_driver/motor_state";
  }

  static const char* value(const ::gripper_driver::motor_state_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::gripper_driver::motor_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 angle\n\
float32 load\n\
";
  }

  static const char* value(const ::gripper_driver::motor_state_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::gripper_driver::motor_state_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.angle);
      stream.next(m.load);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct motor_state_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::gripper_driver::motor_state_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::gripper_driver::motor_state_<ContainerAllocator>& v)
  {
    s << indent << "angle: ";
    Printer<float>::stream(s, indent + "  ", v.angle);
    s << indent << "load: ";
    Printer<float>::stream(s, indent + "  ", v.load);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GRIPPER_DRIVER_MESSAGE_MOTOR_STATE_H