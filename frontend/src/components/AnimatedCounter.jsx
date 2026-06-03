import { motion, useSpring, useTransform } from 'framer-motion';
import { useEffect } from 'react';

const AnimatedCounter = ({ value, decimals = 2, prefix = '', suffix = '' }) => {
  const spring = useSpring(0, { damping: 20, stiffness: 100 });
  useEffect(() => {
    spring.set(value);
  }, [spring, value]);
  const display = useTransform(spring, (current) => 
    `${prefix}${current.toFixed(decimals)}${suffix}`
  );
  return <motion.span>{display}</motion.span>;
};

export default AnimatedCounter;